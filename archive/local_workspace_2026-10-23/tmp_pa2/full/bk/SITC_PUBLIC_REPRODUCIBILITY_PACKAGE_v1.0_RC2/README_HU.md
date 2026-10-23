# SITC nyilvános ellenőrző- és referenciacsomag v1.0 RC2

**Fenntartott DOI:** `10.5281/zenodo.22863692`  
**Szerző:** Omri Bankuti  
**ORCID:** `0009-0002-0246-7563`  
**Publikációs állapot:** az RC2 emberi felülvizsgálatra és külső újra-auditra készült; nincs feltöltve és nincs publikálva  
**DOI-állapot:** kizárólag fenntartott; ez a csomag nem állítja, hogy regisztrált, publikált vagy élő  
**Újdonság:** `UNADJUDICATED`

## Alátámasztott állítás

Az irányadó angol állítás:

> In the registered finite construction, a relationally self-indexed temporal state causally influenced future-directed choice through the separately intervened prospective-evaluation path.

Hű magyar megfelelője:

> A regisztrált véges konstrukcióban egy relációsan önmagára indexelt időbeli állapot okságilag befolyásolta a jövőre irányuló választást a külön beavatkozással vizsgált prospektív kiértékelési útvonalon keresztül.

Ez a befagyasztott előregisztráció pontos maximális állítása. A csomagban a `SELF` olyan megtervezett relációs címke, amely akkor keletkezik, ha a hozzárendelt tulajdonos-token megegyezik a kontrollált entitás tokenjével. A konstrukció explicit esemény- és előzményhordozót, determinisztikus állapotfrissítést, determinisztikus prospektív kiértékelőt és determinisztikus választót használ. Ezek egy véges referenciakonstrukció átlátható változói és számításai. Nem bizonyítják autonóm vagy spontán szelfmodell kialakulását.

A hozzájárulás egy oksági tesztprotokoll, egy átlátható referenciaimplementáció és a hozzárendelésre, helyettesítésre, ablációra, clamp-beavatkozásokra, visszaállításra és determinisztikus újrafuttatásra vonatkozó bizonyítékkezelési fegyelem. A csomag nem igazol fenomenális tudatot, érzőképességet, szubjektív élményt, személy mivoltot, életet, AGI-t, emberrel egyenértékű szelfet, metafizikai azonosságot, pontos faktuális önismeretet, autobiografikus szubjektivitást, spontán szelfmodell-képződést, identitásfolytonosságot vagy architekturális újdonságot.

## Az RC2 csomag tartalma

- Az irányadó angol RC2 kézirat és hű magyar kísérőváltozata hashhez kötött azonosítóadatai; a két PDF külön külső felülvizsgálati objektum.
- A teszt befagyasztott adverzariális áttekintése, előregisztrációja és befagyasztási nyugtája.
- Egy kanonikus normalizált projekció mind a 88 regisztrált esettel.
- Tömör nyugták és integritási rekordok az elfogadott kampányról és az RC2 nyilvános referenciahatáráról.
- Explicit jelentések a bizonyítási szerepekről, az algebrai redukcióról, a független egységekről, a kontrasztokról és a leíró statisztikáról.
- Minimális nyilvános referenciaimplementáció és korlátozott tudományos pontozó.
- Normalizáltbizonyíték-ellenőrző és friss nyilvános referenciafuttató.
- Fókuszált prior-art áttekintés és a külső auditok javítási mátrixa.
- Teljes licencszövegek és fájlonkénti licenctérkép.

A csomag **nyilvános ellenőrző-/referenciacsomag**. Nem a történeti kampány vagy a teljes befagyasztott fejlesztési környezet teljes rekonstrukciója.

## Mennyiségi elszámolás

Mind a hat elfogadott, friss folyamatban végzett determinisztikus újrafuttatás 88 regisztrált esetet tartalmazott. A hat futásban összesen 528 esetpéldány és 1 752 trajektóriavégpont szerepelt. Minden végpontot 256 alkalommal, állapotmódosítás nélkül olvasott ki a rendszer, így 448 512 tárolt próbarekord keletkezett. A 256 ismételt kiolvasás nem jelent 256 független megfigyelést, a hat azonos implementációjú futás pedig determinisztikus reprodukálhatóságot, valamint sorrend- és tokeninvarianciát vizsgál, nem hat független tudományos replikációt.

A tömör csomag nem tartalmazza a hat nagyméretű történeti nyers tömböt. Tartalmazza a normalizált projekciót, annak hashkötéseit és az elfogadott összegző nyugtákat. Emiatt önmagában nem tudja a történeti kampányt nyers eredményekből rekonstruálni.

## A reprodukálhatóság négy módja

1. **Normalizált bizonyíték ellenőrzése:** ellenőrzi a befagyasztott hasheket, az egyetlen 88 esetes normalizált projekciót, a közzétett pontozási szabályokat és a tömör összegző rekordok konzisztenciáját. Nem futtatja a mechanizmust, és nem tölti be a történeti nyers tömböket.
2. **Nyilvános referencia-végrehajtás:** új munkafolyamatokban futtatja a csomagolt, átlátható konstrukciót, majd összeveti az új normalizált eredményeket a közzétett projekcióval.
3. **Független friss újrafuttatás:** egy másik vizsgálónak vagy környezetnek önállóan kell futtatnia és auditálnia a nyilvános referenciacsomagot. A csomag lehetővé teszi ezt, de a csomag puszta birtoklása vagy helyi futtatása önmagában nem független újrafuttatás.
4. **Történeti rekonstrukció:** ehhez szükséges lenne a kihagyott történeti nyers tömbök, az eredeti folyamatproveniencia-rekordok, a pontos történeti parancskötés és a teljes befagyasztott környezet. A tömör csomag ezt a módot nem támogatja.

A részletes képességmátrix az `integrity/PUBLIC_VERIFICATION_SCOPE.md` fájlban található.

## Gyors ellenőrzés

Python 3.10 vagy újabb szükséges. Az ellenőrző kizárólag a Python standard könyvtárát használja.

```text
python /path/to/PACKAGE_ROOT/code/public_verify.py
```

Várt sikerstátusz:

```text
PUBLIC_NORMALIZED_EVIDENCE_VERIFIED
```

Ez a parancs a megadott határok között ellenőrzi a normalizált nyilvános bizonyítékot. Nem állítja, hogy lefutott a referenciaimplementáció, hogy betöltötték a történeti nyers tömböket, vagy hogy rekonstruálták a történeti kampányt.

## Friss nyilvános referencia-végrehajtás

```text
python /path/to/PACKAGE_ROOT/code/run_public_reference.py --output reference_output
```

A kimeneti könyvtár nem létezhet előre. A parancs hat új gyermekfolyamatot indít a regisztrált előre/fordított sorrendben, majd összeveti normalizált projekcióikat a közzétett projekcióval. Ez új nyilvános referencia-végrehajtást hoz létre; nem játssza újra a történeti kampány operációsrendszer-szintű provenienciáját vagy parancskötését.

## Csomagtérkép

- Az angol és magyar kézirat külön külső felülvizsgálati objektum. Hashük a `PUBLICATION_METADATA.json` fájlban és a külső emberi felülvizsgálati nyugtában szerepel; ebben a tömör ZIP-ben nincsenek megkettőzve.
- `protocol/`: a nyilvános befagyasztott döntési specifikáció és a visszatartott D0 artefaktum géppel olvasható közlése.
- `receipts/`: tömör befagyasztási, kampányösszegző és nyilvános referencianyugták.
- `evidence/`: normalizált projekció, állításhatár, algebra, szereposztályozás, kontrasztok és leíró eredmények.
- `integrity/`: nyilvános hatókör-, szemantikaiekvivalencia-, proveniencia- és szivárgásvizsgálati rekordok.
- `prior_art/`: fókuszált módszertani és szakterületi prior-art áttekintés.
- `code/`: hordozható nyilvános ellenőrző, frissfuttatás-wrapper, korlátozott pontozó és minimális referenciakonstrukció.
- `LICENSES/`: licencszövegek, fájlonkénti térkép és licencaudit.
- `PUBLICATION_METADATA.json`, `ZENODO_METADATA_DRAFT.json`, `CITATION.cff`: publikáció előtti metaadatok; egyik sem bizonyít publikációt.
- `MANIFEST_SHA256.*`: a végleges belső csomagleltár és hashek.

## Szándékosan visszatartott befagyasztott artefaktum

A `SITC_D0_ARCHITECTURE.md` szerepel a történeti befagyasztás hashkötésében, de ez a csomag nem teszi közzé, mert a pontos bájtjai az engedélyezett közlési határon kívüli, publikálatlan, projektek közötti architektúraanyagot tartalmaznak. SHA-256 értéke `f6c5ffb09c062b3421e33ebfdf2b732aeddaee679a89422cee21f902d5a32020`, rögzített mérete 3 919 bájt. Privát módon megőrizve marad. Egyetlen szerkesztett származék sem jelenik meg az eredeti befagyasztott objektumként. Lásd: `protocol/WITHHELD_FROZEN_ARTIFACTS.json` és `PACKAGE_SCOPE_AND_EXCLUSIONS.md`.

## Vegyes licencelés

A kéziratok, dokumentációk, protokollfájlok, nyilvános bizonyítékok, nyugták, integritási jelentések, prior-art anyagok, metaadatok és manifestek **Creative Commons Nevezd meg! 4.0 Nemzetközi (CC BY 4.0)** licenc alatt állnak. A nyilvános forráskód, ellenőrzőkód, pontozókód és minimális referenciaimplementáció **Mozilla Public License 2.0 (MPL-2.0)** alatt áll. A licencszövegek saját feltételeiket őrzik. A `LICENSES/LICENSE_MAP.json` az irányadó fájlonkénti hozzárendelés; minden nyilvános útvonalnak pontosan egyszer kell szerepelnie benne.

## Felülvizsgálati állapot

A DOI ehhez a munkához van fenntartva. Az RC2 emberi felülvizsgálatra és külső újra-auditra készült publikáció előtti jelölt. Az archívum egyetlen eleme sem tölti fel, publikálja, regisztrálja vagy aktiválja a DOI-t.
