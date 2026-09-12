"""Synthetic host-transport fixtures, NOT paid execution/isolation evidence.

Only public G IDs and constructed raw bytes are used. No keys, roots, target
generators, State instances, services, filesystem reads or worker callbacks.
"""

from dataclasses import FrozenInstanceError, fields, replace
import struct
import unittest

from e3.protocol import (
    BeginFrame, BindFrame, Capability, ExitFrame, FrameCodec, Kind, Phase,
    ProtocolError, ScalarTag, Service, encode_frame, parse_frame,
)
from e3.transport import (
    Direction, OperationSession, Permit, ScalarOpcode, SessionStage, TransportError,
)


RAW_STATE = bytes(range(256)) + bytes(range(20))
LIVE_STATE = b"\xff" * 276
DEAD_STATE = RAW_STATE[:225] + b"\x00\x00" + RAW_STATE[227:]
EXIT = b"\x03\x14\x01" + LIVE_STATE
SHUTDOWN = b"\x04\x14\x01" + DEAD_STATE
BIND = b"\x00\x08\x00\x09\x00\x01\x00\x04\x00\x00\x00"

# Independent literals: tag, named trace site, direction, exact scalar payload.
SCALARS = (
    (0, ScalarOpcode.TICK_GRANT_E, Direction.IN, b"\x00\x10\x30\x75\x00\x00"),
    (1, ScalarOpcode.TICK_GRANT_P0, Direction.IN, b"\x01\x08\x24\x00\x00\x00"),
    (2, ScalarOpcode.TICK_GRANT_P1, Direction.IN, b"\x02\x08\x00\x00\x00\x00"),
    (3, ScalarOpcode.TICK_GRANT_P2, Direction.IN, b"\x03\x08\xff\x00\x00\x00"),
    (4, ScalarOpcode.TICK_GRANT_P3, Direction.IN, b"\x04\x08\x08\x00\x00\x00"),
    (5, ScalarOpcode.CONTROLLER_OFFER, Direction.IN, b"\x05\x05\x1f\x00\x00\x00"),
    (6, ScalarOpcode.SENSE_E, Direction.IN, b"\x06\x10\xff\xff\x00\x00"),
    (7, ScalarOpcode.SENSE_P, Direction.IN, b"\x07\x08\xff\x00\x00\x00"),
    (8, ScalarOpcode.SELECT_B, Direction.IN, b"\x08\x01\x01\x00\x00\x00"),
    (9, ScalarOpcode.SELECT_T, Direction.IN, b"\x09\x02\x02\x00\x00\x00"),
    (10, ScalarOpcode.SELECT_X, Direction.IN, b"\x0a\x04\x0f\x00\x00\x00"),
    (11, ScalarOpcode.ACTION_REQUEST, Direction.OUT, b"\x0b\x06\x1f\x00\x00\x00"),
    (12, ScalarOpcode.FORAGE_YIELD, Direction.IN, b"\x0c\x10\x40\x00\x00\x00"),
    (13, ScalarOpcode.COLLECT_YIELD, Direction.IN, b"\x0d\x08\x08\x00\x00\x00"),
    (14, ScalarOpcode.RESPONSE_GUESS, Direction.IN, b"\x0e\x01\x01\x00\x00\x00"),
    (15, ScalarOpcode.RESPONSE_BIT, Direction.OUT, b"\x0f\x01\x00\x00\x00\x00"),
    (16, ScalarOpcode.ECOLOGY_YIELD, Direction.IN, b"\x10\x10\x40\x00\x00\x00"),
    (17, ScalarOpcode.LEARNER_RETURN, Direction.IN, b"\x11\x10\x40\x00\x00\x00"),
    (18, ScalarOpcode.ADMIT_CUE, Direction.IN, b"\x12\x04\x0f\x00\x00\x00"),
    (19, ScalarOpcode.LESSON_CUE, Direction.IN, b"\x13\x04\x0f\x00\x00\x00"),
    (20, ScalarOpcode.LESSON_LABEL, Direction.IN, b"\x14\x01\x01\x00\x00\x00"),
    (21, ScalarOpcode.TEMPLATE_CUE, Direction.IN, b"\x15\x04\x0c\x00\x00\x00"),
    (22, ScalarOpcode.TEMPLATE_PAYLOAD, Direction.IN, b"\x16\x04\x01\x00\x00\x00"),
)


def scalar(tag, value=None):
    payload = SCALARS[tag][3]
    if value is not None:
        payload = payload[:2] + struct.pack("<I", value)
    return b"\x02\x06\x00" + payload


def begin(service=Service.CONTROLLER, phase=Phase.DEVELOPMENT, tick=6,
          mask=None, state=RAW_STATE, argument=None):
    if mask is None:
        mask = (4 if phase in (Phase.DEVELOPMENT, Phase.ASSAY, Phase.ECOLOGY)
                and tick >= 6 else 0)
    if argument is None:
        argument = (tick - 1) % 5 if service in (Service.RESPONSE, Service.ADMIT) else 0
    return encode_frame(BeginFrame(phase, tick, service, argument, mask, state))


def session(raw=None, config=4, cap=Capability.ORDINARY):
    s = OperationSession()
    s.accept(encode_frame(BindFrame(config, cap)), Direction.IN)
    if raw is not None:
        s.accept(raw, Direction.IN)
    return s


def send(s, tag, value=None):
    _, opcode, direction, _ = SCALARS[tag]
    token = s.permit(opcode)
    return s.accept(scalar(tag, value), direction, permit=token)


def prefix(s, tags):
    for tag in tags:
        send(s, tag)


class LifecycleTests(unittest.TestCase):
    def assert_failed(self, s):
        self.assertIs(s.stage, SessionStage.FAILED)
        self.assertEqual(s.scalar_count, 0)
        self.assertIsNone(s._begin)
        self.assertIsNone(s._pending)
        for raw, direction in ((BIND, Direction.IN), (begin(), Direction.IN),
                               (EXIT, Direction.OUT), (SHUTDOWN, Direction.OUT)):
            with self.assertRaises(ProtocolError):
                s.accept(raw, direction)
        with self.assertRaises(ProtocolError):
            s.permit(ScalarOpcode.CONTROLLER_OFFER)
        with self.assertRaises(ProtocolError):
            s.finish()

    def test_golden_complete_tick_stream_and_all_returns_none(self):
        s = OperationSession()
        self.assertIs(s.stage, SessionStage.UNBOUND)
        self.assertIsNone(s.binding)
        self.assertIsNone(s.accept(BIND, Direction.IN))
        # Literal BEGIN: development tick 6, TICK, no learning, planned due.
        raw = b"\x01\x1c\x01\x09\x00\x01\x06\x00\x00\x00\x04" + RAW_STATE
        self.assertEqual(parse_frame(raw).state, RAW_STATE)
        self.assertIsNone(s.accept(raw, Direction.IN))
        self.assertIs(s.stage, SessionStage.ACTIVE)
        for tag in range(5):
            self.assertIsNone(send(s, tag))
            self.assertEqual(s.scalar_count, tag + 1)
        self.assertIsNone(s.accept(EXIT, Direction.OUT))
        self.assertIs(s.stage, SessionStage.READY)
        self.assertIsNone(s._begin)
        self.assertEqual(s.scalar_count, 0)
        self.assertIsNone(s.finish())
        self.assertIs(s.stage, SessionStage.CLOSED)

    def test_begin_before_bind_nested_begin_and_duplicate_bind(self):
        for initial in (None, "bound", "active", "completed"):
            s = OperationSession()
            if initial is not None:
                s.accept(BIND, Direction.IN)
            if initial in ("active", "completed"):
                s.accept(begin(), Direction.IN)
            if initial == "completed":
                s.accept(EXIT, Direction.OUT)
            raw = begin() if initial in (None, "active") else BIND
            with self.assertRaises(ProtocolError):
                s.accept(raw, Direction.IN)
            self.assert_failed(s)
        # Identical and changed BINDs are both forbidden, even during BEGIN.
        for config in (4, 204):
            s = session(begin())
            with self.assertRaises(ProtocolError):
                s.accept(encode_frame(BindFrame(config)), Direction.IN)
            self.assert_failed(s)

    def test_unbound_idle_and_terminal_outputs_rejected(self):
        for initial in ("unbound", "ready", "closed", "shutdown"):
            for raw in (EXIT, SHUTDOWN, scalar(5)):
                s = OperationSession() if initial == "unbound" else session()
                if initial == "closed":
                    s.finish()
                if initial == "shutdown":
                    s.accept(begin(), Direction.IN)
                    s.accept(SHUTDOWN, Direction.OUT)
                with self.assertRaises(ProtocolError):
                    s.accept(raw, Direction.OUT)
                self.assert_failed(s)

    def test_strict_frame_directions_and_direction_enum(self):
        for raw, s in ((BIND, OperationSession()), (begin(), session()),
                       (EXIT, session(begin())), (SHUTDOWN, session(begin()))):
            wrong = Direction.OUT if raw[0] in (0, 1) else Direction.IN
            with self.assertRaises(ProtocolError):
                s.accept(raw, wrong)
            self.assert_failed(s)
        for bad in (True, False, 0, 1, Kind.BIND, "IN", None):
            s = OperationSession()
            with self.assertRaises(ProtocolError):
                s.accept(BIND, bad)
            self.assert_failed(s)
        for tag, preceding, raw in ((5, (), begin()),
                                    (11, range(5, 11), begin()),
                                    (15, (), begin(Service.RESPONSE))):
            s = session(raw)
            prefix(s, preceding)
            token = s.permit(SCALARS[tag][1])
            wrong = Direction.OUT if token.direction is Direction.IN else Direction.IN
            with self.assertRaises(ProtocolError):
                s.accept(scalar(tag), wrong, permit=token)
            self.assert_failed(s)

    def test_raw_bytes_preserved_not_owned_worker_state(self):
        s = session(begin(state=LIVE_STATE))
        self.assertEqual(s._begin.state, LIVE_STATE)
        with self.assertRaises(FrozenInstanceError):
            s._begin.state = DEAD_STATE
        # EXIT's payload is actual output, not compared to or replaced by BEGIN.
        changed = RAW_STATE
        self.assertIsNone(s.accept(encode_frame(ExitFrame(changed)), Direction.OUT))
        self.assertIsNone(s._begin)
        self.assertIsNone(s._cue)
        s.accept(begin(Service.RESPONSE, Phase.RECOVERY, tick=1,
                       state=DEAD_STATE), Direction.IN)
        self.assertEqual(s._begin.state, DEAD_STATE)
        # No economic inference or revival proof: raw BEGIN accepts dead bytes.
        s.accept(SHUTDOWN, Direction.OUT)
        self.assertIsNone(s._begin)
        self.assertEqual(LIVE_STATE, b"\xff" * 276)
        self.assertEqual(DEAD_STATE[227:], RAW_STATE[227:])

    def test_exit_positive_energy_shutdown_zero_and_no_wiping(self):
        for energy in (1, 256, 65535):
            raw = RAW_STATE[:225] + struct.pack("<H", energy) + RAW_STATE[227:]
            s = session(begin())
            s.accept(b"\x03\x14\x01" + raw, Direction.OUT)
            s = session(begin())
            with self.assertRaises(ProtocolError):
                s.accept(b"\x04\x14\x01" + raw, Direction.OUT)
            self.assert_failed(s)
        s = session(begin())
        with self.assertRaises(ProtocolError):
            s.accept(b"\x03\x14\x01" + DEAD_STATE, Direction.OUT)
        self.assert_failed(s)
        s = session(begin())
        self.assertIsNone(s.accept(SHUTDOWN, Direction.OUT))
        self.assertIs(s.stage, SessionStage.CLOSED)
        self.assertEqual(parse_frame(SHUTDOWN).state, DEAD_STATE)

    def test_eof_and_abort_cannot_silently_complete_an_operation(self):
        for tags in ((), (5,), tuple(range(5, 11)), tuple(range(5, 12)) + (13,)):
            s = session(begin())
            prefix(s, tags)
            with self.assertRaises(ProtocolError):
                s.finish()
            self.assert_failed(s)
        s = OperationSession()
        with self.assertRaises(ProtocolError):
            s.finish()
        s = session(begin())
        with self.assertRaises(ProtocolError):
            s.abort()
        self.assert_failed(s)
        s = session()  # Fixed finite sequence may be empty, but still BIND once.
        s.finish()

    def test_malformed_current_packet_is_terminal_not_retry_or_shutdown(self):
        good = scalar(5)
        malformed = [good[:n] for n in range(len(good))]
        malformed += [good + b"\x00", good + good, b"\xff\x00\x00",
                      b"\x02\x05\x00" + good[3:],
                      b"\x02\x06\x00\xff\x05\x00\x00\x00\x00",
                      b"\x02\x06\x00\x05\x04\x00\x00\x00\x00",
                      scalar(5, 32), bytearray(good), memoryview(good),
                      {}, [], None, lambda: good]
        for raw in malformed:
            s = session(begin())
            token = s.permit(ScalarOpcode.CONTROLLER_OFFER)
            with self.assertRaises(ProtocolError):
                s.accept(raw, Direction.IN, permit=token)
            self.assert_failed(s)


class PermitTests(unittest.TestCase):
    def test_frozen_narrow_descriptor_no_callback_or_receipt(self):
        s = session(begin())
        token = s.permit(ScalarOpcode.CONTROLLER_OFFER)
        self.assertEqual([f.name for f in fields(token)], ["opcode"])
        self.assertFalse(hasattr(token, "__dict__"))
        self.assertFalse(hasattr(s, "__dict__"))
        self.assertIs(token.tag, ScalarTag.OFFER)
        self.assertIs(token.direction, Direction.IN)
        with self.assertRaises(FrozenInstanceError):
            token.opcode = ScalarOpcode.SENSE_E
        with self.assertRaises(AttributeError):
            s.binding = BindFrame(204)
        with self.assertRaises(FrozenInstanceError):
            s.binding.capability = Capability.TEMPLATE
        for extra in ({"paid": True}, {"receipt": True}, {"producer": lambda: 0},
                      {"state": RAW_STATE}, {"root": b"x" * 32}):
            with self.assertRaises(TypeError):
                Permit(ScalarOpcode.CONTROLLER_OFFER, **extra)
            with self.assertRaises(TypeError):
                OperationSession(**extra)
        for bad in (True, False, 5, ScalarTag.OFFER, Service.REP_LESSON,
                    "CONTROLLER_OFFER", lambda: True):
            with self.assertRaises(ProtocolError):
                Permit(bad)
            s = session(begin())
            with self.assertRaises(ProtocolError):
                s.permit(bad)
            self.assertIs(s.stage, SessionStage.FAILED)

    def test_one_shot_not_equal_copy_stale_or_other_session(self):
        for mode in ("missing", "forged", "copy", "other", "bool"):
            s = session(begin())
            current = s.permit(ScalarOpcode.CONTROLLER_OFFER)
            other = session(begin())
            token = {"missing": None, "forged": Permit(current.opcode),
                     "copy": replace(current),
                     "other": other.permit(current.opcode), "bool": True}[mode]
            with self.assertRaises(ProtocolError):
                s.accept(scalar(5), Direction.IN, permit=token)
            self.assertIs(s.stage, SessionStage.FAILED)
        s = session(begin())
        old = s.permit(ScalarOpcode.CONTROLLER_OFFER)
        s.accept(scalar(5), Direction.IN, permit=old)
        with self.assertRaises(ProtocolError):
            s.accept(scalar(5), Direction.IN, permit=old)
        self.assertIs(s.stage, SessionStage.FAILED)

    def test_no_prefetch_skip_repeated_grant_or_tag_override(self):
        s = session(begin(Service.TICK))
        token = s.permit(ScalarOpcode.TICK_GRANT_E)
        with self.assertRaises(ProtocolError):
            s.permit(ScalarOpcode.TICK_GRANT_P0)
        self.assertIsNone(s._pending)
        for bad_tag in (0, 2, 5):
            s = session(begin(Service.TICK))
            send(s, 0)
            with self.assertRaises(ProtocolError):
                s.permit(SCALARS[bad_tag][1])
        s = session(begin(Service.TICK))
        token = s.permit(ScalarOpcode.TICK_GRANT_E)
        with self.assertRaises(ProtocolError):
            s.accept(scalar(1), Direction.IN, permit=token)
        self.assertEqual(s.scalar_count, 0)

    def test_pending_input_forbids_exit_but_shutdown_allows_prefix(self):
        for service, opcode in ((Service.CONTROLLER, ScalarOpcode.CONTROLLER_OFFER),
                                (Service.ADMIT, ScalarOpcode.ADMIT_CUE)):
            s = session(begin(service))
            s.permit(opcode)
            with self.assertRaises(ProtocolError):
                s.accept(EXIT, Direction.OUT)
            s = session(begin(service))
            s.permit(opcode)
            s.accept(SHUTDOWN, Direction.OUT)
            self.assertIsNone(s._pending)
        s = session(begin())
        token = s.permit(ScalarOpcode.CONTROLLER_OFFER)
        with self.assertRaises(ProtocolError):
            s.accept(SHUTDOWN, Direction.OUT, permit=token)

    def test_budget_eight_counts_both_directions_and_resets_per_begin(self):
        s = session()
        for tick in (6, 7, 8):
            s.accept(begin(tick=tick), Direction.IN)
            for tag in (*range(5, 12), 13):
                send(s, tag)
            self.assertEqual(s.scalar_count, 8)
            s.accept(EXIT, Direction.OUT)
            self.assertEqual(s.scalar_count, 0)
        s.accept(begin(), Direction.IN)
        prefix(s, (*range(5, 12), 13))
        with self.assertRaisesRegex(ProtocolError, "budget"):
            s.permit(ScalarOpcode.COLLECT_YIELD)
        self.assertIs(s.stage, SessionStage.FAILED)


class ServiceFlowTests(unittest.TestCase):
    def test_all_twenty_three_tags_accepted_in_complete_paths(self):
        cases = [
            (4, 0, begin(Service.TICK), tuple(range(5))),
            (4, 0, begin(), (*range(5, 12), 13)),
            (104, 0, begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), (14, 15, 16, 17)),
            (4, 0, begin(Service.ADMIT), (18,)),
            (4, 0, begin(Service.REP_LESSON, Phase.ACQUISITION, tick=1), (19, 20)),
            (204, 0, begin(Service.BLOCK_LESSON, Phase.ACQUISITION, tick=1), (19, 20)),
            (4, 1, begin(Service.TEMPLATE, Phase.ORACLE, tick=0), (21, 22)),
        ]
        covered = set()
        for config, cap, raw, tags in cases:
            s = session(raw, config, cap)
            prefix(s, tags)
            covered.update(tags)
            s.accept(EXIT, Direction.OUT)
        s = session(begin())
        prefix(s, range(5, 11))
        send(s, 11, 15)  # Forage, current cue 15.
        send(s, 12)
        s.accept(EXIT, Direction.OUT)
        covered.add(12)
        self.assertEqual(covered, set(range(23)))

    def test_complete_prefixes_and_shutdown_at_every_scalar_stage(self):
        cases = [
            (4, 0, begin(Service.TICK), tuple(range(5)), {5}),
            (4, 0, begin(), (*range(5, 12), 13), {0, 6, 8}),
            (99, 0, begin(mask=5), (*range(5, 12), 13), {0, 6, 8}),
            (9, 0, begin(), (5, 6, 7, 11, 13), {0, 3, 5}),
            (90, 0, begin(), (5, 6, 7, 11, 13), {0, 3, 5}),
            (400, 0, begin(phase=Phase.ECOLOGY, mask=7), (5, 6, 7, 11, 13), {0, 3, 5}),
            (104, 0, begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), (14, 15, 16, 17), {0, 4}),
            (104, 0, begin(Service.RESPONSE, Phase.ECOLOGY, mask=4), (14, 15, 16), {0, 3}),
            (4, 0, begin(Service.RESPONSE, Phase.ASSAY), (14, 15), {0, 2}),
            (4, 0, begin(Service.RESPONSE, Phase.RECOVERY), (15,), {0, 1}),
            (4, 0, begin(Service.ADMIT), (18,), {0, 1}),
            (4, 0, begin(Service.REP_LESSON, Phase.ACQUISITION, tick=1), (19, 20), {0, 2}),
            (204, 0, begin(Service.BLOCK_LESSON, Phase.ACQUISITION, tick=1), (19, 20), {0, 2}),
            (204, 1, begin(Service.TEMPLATE, Phase.ORACLE, tick=0), (21, 22), {0, 2}),
        ]
        for config, cap, raw, tags, complete in cases:
            for n in range(len(tags) + 1):
                for ending in (EXIT, SHUTDOWN):
                    with self.subTest(config=config, tags=tags, n=n, ending=ending[0]):
                        s = session(raw, config, cap)
                        prefix(s, tags[:n])
                        if ending == SHUTDOWN or n in complete:
                            s.accept(ending, Direction.OUT)
                        else:
                            with self.assertRaises(ProtocolError):
                                s.accept(ending, Direction.OUT)
                            self.assertIs(s.stage, SessionStage.FAILED)

    def test_no_scalar_services_and_empty_rejections(self):
        cases = [(Service.COMMIT, Phase.ACQUISITION, 4, 0),
                 (Service.TERMINAL, Phase.DEVELOPMENT, 2048, 5),
                 (Service.ISOLATE, Phase.RECOVERY, 0, 0),
                 (Service.AGE_LOW, Phase.DEVELOPMENT, 6, 4),
                 (Service.AGE_HIGH, Phase.DEVELOPMENT, 6, 4),
                 (Service.CONDITION, Phase.DEVELOPMENT, 6, 4)]
        for service, phase, tick, mask in cases:
            raw = begin(service, phase, tick, mask)
            s = session(raw, 204)
            s.accept(EXIT, Direction.OUT)
            for _, opcode, _, _ in SCALARS:
                s = session(raw, 204)
                with self.assertRaises(ProtocolError):
                    s.permit(opcode)

    def test_exact_order_cannot_skip_or_repeat_each_mandatory_group(self):
        cases = [(begin(Service.TICK), (0, 1, 2, 3, 4)),
                 (begin(), (5, 6, 7, 8, 9, 10, 11, 13)),
                 (begin(Service.REP_LESSON, Phase.ACQUISITION, tick=1), (19, 20)),
                 (begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), (14, 15, 16, 17))]
        for raw, tags in cases:
            for index, tag in enumerate(tags):
                s = session(raw)
                prefix(s, tags[:index + 1])
                with self.assertRaises(ProtocolError):
                    s.permit(SCALARS[tag][1])
            for i in range(len(tags) - 1):
                # RESPONSE may omit GUESS, all other adjacent swaps are invalid.
                if tags[i] == 14:
                    continue
                s = session(raw)
                prefix(s, tags[:i])
                with self.assertRaises(ProtocolError):
                    s.permit(SCALARS[tags[i + 1]][1])

    def test_controller_requests_action_cue_matching_yield_and_no_scrub_packet(self):
        for action in (0, 1):
            for cue in range(16):
                s = session(begin())
                send(s, 5, cue | 16)
                prefix(s, range(6, 11))
                send(s, 11, (action << 4) | cue)
                self.assertEqual(s._action, action)
                send(s, 12 + action, 0)
                self.assertIsNone(s._action)
                s.accept(EXIT, Direction.OUT)
                s = session(begin())
                send(s, 5, cue)
                prefix(s, range(6, 11))
                send(s, 11, (action << 4) | cue)
                with self.assertRaises(ProtocolError):
                    s.permit(SCALARS[13 - action][1])
        for bad in (*range(32, 64), 0, 16):
            s = session(begin())
            prefix(s, range(5, 11))  # Offer cue=15, not zero.
            with self.assertRaises(ProtocolError):
                send(s, 11, bad)
            self.assertIs(s.stage, SessionStage.FAILED)
        s = session(begin())
        prefix(s, range(5, 11))
        # Action 2, rejected ACTION and abstention have the same scalar shape.
        s.accept(EXIT, Direction.OUT)

    def test_fixed_and_scripts_never_receive_ranks_frozen_rl_and_drive_do(self):
        for config in (9, 90, 209, 290, *range(400, 404)):
            raw = (begin(phase=Phase.ECOLOGY, mask=7) if config >= 400 else begin())
            for tag in (8, 9, 10):
                s = session(raw, config)
                prefix(s, (5, 6, 7))
                with self.assertRaises(ProtocolError):
                    s.permit(SCALARS[tag][1])
            s = session(raw, config)
            prefix(s, (5, 6, 7, 11, 13))
            self.assertEqual(s.scalar_count, 5)
            s.accept(EXIT, Direction.OUT)
        for config in (4, 104, 204, 304, 99, 199, 299, 399):
            for mask in (4, 5, 6, 7):
                s = session(begin(mask=mask), config)
                prefix(s, range(5, 11))
                s.accept(EXIT, Direction.OUT)

    def test_response_unique_guess_due_learning_and_pair_consistency(self):
        for phase in (Phase.DEVELOPMENT, Phase.ECOLOGY):
            for learning in (0, 1):
                for guessed in (False, True):
                    for tick in (1, 5, 6, 7):
                        due = tick >= 6
                        for y, b in ((0, 0), (0, -64), (64, 64)):
                            s = session(begin(Service.RESPONSE, phase, tick,
                                              learning | (4 if due else 0)), 104)
                            if guessed:
                                send(s, 14)
                            send(s, 15)
                            if due:
                                send(s, 16, y)
                                if learning:
                                    send(s, 17, b & 65535)
                            s.accept(EXIT, Direction.OUT)
        for y, b in ((0, 64), (64, 0), (64, -64)):
            s = session(begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), 104)
            send(s, 15)
            send(s, 16, y)
            with self.assertRaises(ProtocolError):
                send(s, 17, b & 65535)
            self.assertIs(s.stage, SessionStage.FAILED)

    def test_feedback_absent_not_a_zero_or_free_due_cue(self):
        for phase, tick, mask in ((Phase.RECOVERY, 6, 0), (Phase.ASSAY, 6, 4),
                                  (Phase.DEVELOPMENT, 1, 1), (Phase.ECOLOGY, 5, 1)):
            for tag in (16, 17):
                s = session(begin(Service.RESPONSE, phase, tick, mask), 104)
                send(s, 15)
                with self.assertRaises(ProtocolError):
                    s.permit(SCALARS[tag][1])
        for tag in (16, 17):
            s = session(begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), 104)
            with self.assertRaises(ProtocolError):
                s.permit(SCALARS[tag][1])
        s = session(begin(Service.RESPONSE, Phase.ECOLOGY, mask=4), 104)
        prefix(s, (15, 16))
        with self.assertRaises(ProtocolError):
            s.permit(ScalarOpcode.LEARNER_RETURN)

    def test_template_capability_header_semantic_bad_is_not_paid_validation(self):
        raw = begin(Service.TEMPLATE, Phase.ORACLE, tick=0)
        for config in (4, 204):
            s = session(config=config)
            with self.assertRaises(ProtocolError):
                s.accept(raw, Direction.IN)
            s = session(raw, config, Capability.TEMPLATE)
            s.accept(EXIT, Direction.OUT)  # Body rejection: no input.
            for cue, payload in ((0, 0), (4, 1), (12, 1)):
                s = session(raw, config, Capability.TEMPLATE)
                send(s, 21, cue)
                send(s, 22, payload)
                s.accept(EXIT, Direction.OUT)
        # Structurally valid BAD packets are consumed in order, never masked;
        # actual paid G BAD/S remains pending. No successful result is allowed.
        for config, cue, payload in ((4, 15, 2), (204, 3, 15)):
            for ending in (EXIT, SHUTDOWN):
                s = session(raw, config, Capability.TEMPLATE)
                self.assertIsNone(send(s, 21, cue))
                self.assertIsNone(send(s, 22, payload))
                self.assertIs(s.stage, SessionStage.ACTIVE)
                self.assertEqual(s.scalar_count, 2)
                with self.assertRaisesRegex(ProtocolError, "semantic BAD"):
                    s.accept(ending, Direction.OUT)
                self.assertIs(s.stage, SessionStage.FAILED)
        s = session(raw, 204, Capability.TEMPLATE)
        send(s, 21, 3)
        send(s, 22, 15)
        with self.assertRaises(ProtocolError):
            s.abort()  # Future host routes actual BAD completion to failure.

    def test_template_semantic_check_does_not_precede_second_input(self):
        raw = begin(Service.TEMPLATE, Phase.ORACLE, tick=0)
        for pending in (False, True):
            s = session(raw, 204, Capability.TEMPLATE)
            send(s, 21, 3)  # Width-valid unaligned cue, not yet the G BAD site.
            if pending:
                s.permit(ScalarOpcode.TEMPLATE_PAYLOAD)
            s.accept(SHUTDOWN, Direction.OUT)
            self.assertIs(s.stage, SessionStage.CLOSED)
            self.assertIsNone(s._begin)
            self.assertIsNone(s._pending)
        s = session(raw, 204, Capability.TEMPLATE)
        send(s, 21, 3)
        with self.assertRaisesRegex(ProtocolError, "mandatory scalar group"):
            s.accept(EXIT, Direction.OUT)

    def test_scalar_site_permissions_not_arbitrary_service_tags(self):
        cases = [
            (4, 0, begin(Service.TICK), {0}),
            (4, 0, begin(), {5}),
            (104, 0, begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), {14, 15}),
            (4, 0, begin(Service.ADMIT), {18}),
            (4, 0, begin(Service.REP_LESSON, Phase.ACQUISITION, tick=1), {19}),
            (204, 0, begin(Service.BLOCK_LESSON, Phase.ACQUISITION, tick=1), {19}),
            (204, 1, begin(Service.TEMPLATE, Phase.ORACLE, tick=0), {21}),
        ]
        for config, cap, raw, first in cases:
            for tag, opcode, _, _ in SCALARS:
                s = session(raw, config, cap)
                if tag in first:
                    token = s.permit(opcode)
                    self.assertIs(token.tag, ScalarTag(tag))
                else:
                    with self.assertRaises(ProtocolError):
                        s.permit(opcode)
                    self.assertIs(s.stage, SessionStage.FAILED)


class ContextBoundaryTests(unittest.TestCase):
    def test_current_begin_revalidated_with_actual_codec(self):
        # Every body is structurally valid but violates its selected BIND.
        cases = [(4, begin(Service.BLOCK_LESSON, Phase.ACQUISITION, 4)),
                 (204, begin(Service.REP_LESSON, Phase.ACQUISITION, 4)),
                 (9, begin(mask=5)), (90, begin(mask=5)),
                 (400, begin()), (401, begin(phase=Phase.ECOLOGY, mask=4))]
        for config, raw in cases:
            frame = parse_frame(raw)
            with self.assertRaises(ProtocolError):
                FrameCodec(BindFrame(config)).validate(frame)
            s = session(config=config)
            with self.assertRaises(ProtocolError):
                s.accept(raw, Direction.IN)
            self.assertIs(s.stage, SessionStage.FAILED)
        # Raw field violations: unknown phase/service, reserved mask, slot,
        # drain ADMIT, template phase/tick/argument. No normalization.
        base = begin(Service.RESPONSE)
        malformed = [base[:i] + bytes((v,)) + base[i + 1:]
                     for i, v in ((5, 255), (8, 255), (9, 5), (10, 255))]
        drain = begin(Service.RESPONSE, Phase.ECOLOGY, tick=512)
        malformed.append(drain[:8] + bytes((Service.ADMIT,)) + drain[9:])
        oracle = begin(Service.TEMPLATE, Phase.ORACLE, tick=0)
        malformed += [oracle[:i] + b"\x01" + oracle[i + 1:] for i in (6, 9, 10)]
        for raw in malformed:
            s = session(cap=Capability.TEMPLATE)
            with self.assertRaises(ProtocolError):
                s.accept(raw, Direction.IN)
            self.assertIs(s.stage, SessionStage.FAILED)

    def test_drains_slot_rotation_and_sequential_services_same_binding(self):
        for config, phase, last, mask in ((4, Phase.DEVELOPMENT, 2048, 5),
                                          (104, Phase.ECOLOGY, 512, 5),
                                          (4, Phase.ASSAY, 261, 4),
                                          (400, Phase.ECOLOGY, 512, 7)):
            s = session(config=config)
            for tick in range(last - 4, last + 1):
                s.accept(begin(Service.TICK, phase, tick, mask), Direction.IN)
                prefix(s, range(5))
                s.accept(EXIT, Direction.OUT)
                if phase is not Phase.ASSAY:
                    s.accept(begin(Service.CONTROLLER, phase, tick, mask), Direction.IN)
                    prefix(s, (5, 6, 7) if config == 400 else range(5, 11))
                    s.accept(EXIT, Direction.OUT)
                s.accept(begin(Service.RESPONSE, phase, tick, mask), Direction.IN)
                send(s, 15)
                if phase is not Phase.ASSAY:
                    prefix(s, (16, 17))
                s.accept(EXIT, Direction.OUT)
            self.assertEqual(s.binding.public_config_id, config)
            s.finish()

    def test_new_begin_does_not_inherit_due_learning_or_old_input_references(self):
        s = session(begin(Service.RESPONSE, Phase.ECOLOGY, mask=5), 104)
        prefix(s, (14, 15, 16, 17))
        s.accept(EXIT, Direction.OUT)
        self.assertTrue(all(getattr(s, name) is None for name in
                            ("_begin", "_pending", "_cue", "_action", "_yield", "_last")))
        s.accept(begin(Service.RESPONSE, Phase.RECOVERY, tick=1, state=LIVE_STATE), Direction.IN)
        send(s, 15)
        s.accept(EXIT, Direction.OUT)
        # Old token cannot be reused on the same site in the next operation.
        s.accept(begin(phase=Phase.RECOVERY), Direction.IN)
        token = s.permit(ScalarOpcode.CONTROLLER_OFFER)
        s.accept(scalar(5), Direction.IN, permit=token)
        prefix(s, range(6, 11))
        s.accept(EXIT, Direction.OUT)
        s.accept(begin(phase=Phase.RECOVERY), Direction.IN)
        s.permit(ScalarOpcode.CONTROLLER_OFFER)
        with self.assertRaises(ProtocolError):
            s.accept(scalar(5), Direction.IN, permit=token)
        self.assertIs(s.stage, SessionStage.FAILED)

    def test_reset_capability_requires_new_host_context_never_rebind(self):
        privileged = session(begin(Service.TEMPLATE, Phase.ORACLE, tick=0),
                             cap=Capability.TEMPLATE)
        prefix(privileged, (21, 22))
        privileged.accept(EXIT, Direction.OUT)
        privileged.finish()  # External lifecycle closes/cancels old context.
        with self.assertRaises(ProtocolError):
            privileged.accept(BIND, Direction.IN)
        ordinary = session(begin(Service.ISOLATE, Phase.RECOVERY, tick=0))
        self.assertIs(ordinary.binding.capability, Capability.ORDINARY)
        ordinary.accept(EXIT, Direction.OUT)
        with self.assertRaises(ProtocolError):
            ordinary.accept(begin(Service.TEMPLATE, Phase.ORACLE, tick=0), Direction.IN)


if __name__ == "__main__":
    unittest.main()