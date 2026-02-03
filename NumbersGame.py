operatsioonid = ["+", "/", "*", "-"]
from copy import deepcopy

def main():
    print("Tere tulemast numbrimängu lahendajasse! Teeme kõik su levelid ära!!")
    tabel = input("Kui suur on teie tabel? (Rida)x(Veerg) ")
    arvud = input("Sisestage arvud, mis on teie tabelis. (Eraldatud tühikuga) ")
    vajaliktulemus = input("Sisesta vajalikud tulemused. (Eralda tühikuga) ")
    laud,vastus = tabelisisu(tabel, arvud, vajaliktulemus)
    print("Alglaud: ")
    for i in laud:
        print(i)
    print("Siht (viimane rida): ",vastus)
    kaigud = genereeriK2igud(laud)
    print("Käike:", len(kaigud))
    if kaigud:
        print("Testkäik:", kaigud[0])
        uus = rakendaK2ik(laud, kaigud[0])
        print("Pärast käiku: ")
        for rida in uus:
            print(rida)
    tee = lahenda(laud, vastus)

    if tee is None:
        print("Lahendust ei leitud.")
    else:
        print("Leitud lahendus, käigud:")
        for i, k in enumerate(tee, start=1):
            print(i, prindi_kaik(k))


def tabelisisu(tabel, arvud,vajaliktulemus):
    nimekiriarvudest = []
    nimekirivastustest = []

    osad = vajaliktulemus.split()
    for i in osad:
        nimekirivastustest.append(int(i))

    osad1 = tabel.split("x")

    ridadearv = int(osad1[0])
    veergudearv = int(osad1[1])

    read = []
    for i in range(int(ridadearv)):
        read.append([])

    for s in arvud.split():
        nimekiriarvudest.append(int(s))
    laud = listieraldaja(nimekiriarvudest,read,ridadearv,veergudearv)
    return laud, nimekirivastustest

def listieraldaja(nimekiriarvudest,read,ridadearv,veergudearv):
    for i in range(ridadearv):
        start = i * veergudearv
        end = start + veergudearv
        read[i] = (nimekiriarvudest[start:end])
    return(read)

def lubatudtehe(a,b,op):
    if a is None or b is None:
        return False
    if op == "+":
        return True
    if op == "/":
        return b!=0 and (a % b == 0) and (a//b>0)
    if op == "*":
        return True
    if op == "-":
        return (a-b)>0
    return False

def arvutamistehe(a,b,op):
    if op == "+":
        return a+b
    if op == "/":
        return a//b
    if op == "*":
        return a*b
    if op == "-":
        return a-b

def naabrid(r, c, ridadearv, veergudearv):
    tulemused = []
    suunad = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for dr, dc in suunad:
        nr, nc = r+dr, c+dc
        if 0<=nr<ridadearv and 0<=nc<veergudearv:
            tulemused.append((nr,nc))
    return tulemused

def genereeriK2igud(read):
    ridadearv = len(read)
    veergudearv = len(read[0])
    k2igud = []
    viimanerida = ridadearv-1
    for r in range(ridadearv):
        for c in range(veergudearv):
            a = read[r][c]
            if a is None:
                continue

            for nr, nc in naabrid(r,c,ridadearv, veergudearv):
                if r == viimanerida:
                    if nr < r:
                        continue

                    if nr == r and abs(nc - c) == 1:
                        if read[r - 1][c] is None:
                            continue
                    else:
                        continue

                b = read[nr][nc]
                if b is None:
                    continue

                for op in operatsioonid:
                    if lubatudtehe(a,b,op):
                        k2igud.append((r,c,nr,nc,op))

    return k2igud

def gravity(laud):
    ridasid = len(laud)
    veerge = len(laud[0])

    for c in range(veerge):
        veeru_numbrid = []
        for r in range(ridasid):
            if laud[r][c] is not None:
                veeru_numbrid.append(laud[r][c])

        # täida alt üles
        for r in range(ridasid - 1, -1, -1):
            if veeru_numbrid:
                laud[r][c] = veeru_numbrid.pop()
            else:
                laud[r][c] = None

    return laud

def rakendaK2ik(read, kaik):
    r,c,nr,nc,op = kaik
    ridadearv = len(read)
    veergudearv = len(read[0])
    viimanerida = ridadearv-1

    a = read[r][c]
    b = read[nr][nc]

    if a is None or b is None:
        return None

    if (nr,nc) not in naabrid(r,c,ridadearv, veergudearv):
        return None
    if r == viimanerida:
        if nr<r:
            return None
        if not (nr==r and abs(nc-c)==1):
            return None
        if read[r-1][c] is None:
            return None

    #tehted
    if not lubatudtehe(a,b,op):
        return None
    tulemus = arvutamistehe(a,b,op)
    if tulemus == 0:
        return None
    uus = deepcopy(read)
    uus[nr][nc]=tulemus
    uus[r][c]=None
    gravity(uus)
    return uus

def lauavoti(laud):
    uus = []
    for rida in laud:
        uus.append(tuple(rida))
    return tuple(uus)

def on_voit(laud, vastus):
    # 1) viimane rida peab olema täpselt vastus
    if laud[-1] != vastus:
        return False

    # 2) kõik read peale viimase peavad olema tühjad (None)
    for r in range(len(laud) - 1):
        for x in laud[r]:
            if x is not None:
                return False

    return True


def max_sammud(laud):
    ridadearv = len(laud)
    veergudearv = len(laud[0])
    return ridadearv * veergudearv - veergudearv

def lahenda(laud, vastus):
    sammudelimiit = max_sammud(laud)
    proovitudk2igud = set()

    def dfs(seis,samme_jaanud,kaigutee):
        voti = lauavoti(seis)
        if (voti, samme_jaanud) in proovitudk2igud:
            return None
        proovitudk2igud.add((voti, samme_jaanud))
        if on_voit(seis, vastus):
            return kaigutee
        if samme_jaanud == 0:
            return None
        kaigud = genereeriK2igud(seis)

        for kaik in kaigud:
            uus_seis = rakendaK2ik(seis, kaik)
            if uus_seis is None:
                continue
            tulemus = dfs(uus_seis, samme_jaanud - 1, kaigutee + [kaik])
            if tulemus is not None:
                return tulemus
        return None
    return dfs(laud, sammudelimiit, [])

def prindi_kaik(kaik):
    r, c, nr, nc, op = kaik
    return f"({r},{c}) -> ({nr},{nc})  {op}"

main()











