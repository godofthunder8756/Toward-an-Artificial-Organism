"""Verify: do the surviving 'majority' individuals actually restore the corrupted bits' majority?

The sweep showed the cheaper (majority-only) write extends survival to n=32/64 where `full` and
`staged` die. But survival alone could be confounded (an organism that muddles through wrong). This
checks the surviving rows' `corrupted_still_wrong` and `program_correct` -- does the cheaper write
actually recover the corrupted content, or merely survive?
"""
import ac76_recovery_probe as rp

if __name__ == '__main__':
    print('majority variant, per-individual: corrupted bits still wrong vs program correct')
    for nbits in (16, 32, 64):
        print(f'  nbits={nbits}:')
        for s in (0, 1, 2, 3):
            for h in (0, 1):
                r = rp.run(s, h, 'majority', nbits)
                print(f'    seed={s} hist={h}: completed={r["completed"]} dead={r["first_dead"]} '
                      f'still_wrong={r["corrupted_still_wrong"]}/{nbits} '
                      f'program_correct={r["program_correct"]}/126 reg_writes={r["reg_writes"]}')
