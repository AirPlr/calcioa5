import random
import os
risp=''

def printskip(stringa):
    if risp=='no':
        print(stringa)
# Funzione per simulare una partita tra due squadre
def partita(giocatori1, giocatori2, marcatori):
    gol1= 0
    gol2 = 0
    totale_gol_partita = random.randint(0, 10)
    for i in range(totale_gol_partita):
        for giocatore in giocatori1:
            if random.random() < 0.01 * giocatore['abilità']:
                gol1 += 1
                aggiorna_marcatori(marcatori, giocatore['nome'])
                break
        for giocatore in giocatori2:
            if random.random() < 0.01 * giocatore['abilità']:
                gol2 += 1
                aggiorna_marcatori(marcatori, giocatore['nome'])
                break
    return gol1, gol2

# Funzione per aggiornare la classifica marcatori
def aggiorna_marcatori(marcatori, nome_giocatore):
    for marcatore in marcatori:
        if marcatore[0] == nome_giocatore:
            marcatori.remove(marcatore)
            marcatori.add((nome_giocatore, marcatore[1] + 1))
            return
    marcatori.add((nome_giocatore, 1))

# Funzione per stampare il risultato della partita
def stampa_risultato(nome_squadra1, nome_squadra2, gol1, gol2):
    printskip(f"{nome_squadra1} {gol1} - {gol2} {nome_squadra2}")

# Funzione per generare un file template con i giocatori
def genera_template(nome_file):
    with open(nome_file, 'w') as file:
        for p in range(36):
            file.write(f"Giocatore{p}, {random.randint(1, 10)}\n")

# Funzione per generare la struttura del torneo
def genera_struttura_torneo(squadre):
    num_squadre = len(squadre)
    partite = []
    for turno in range(num_squadre - 1):
        giornata = []
        for i in range(num_squadre // 2):
            squadra1 = squadre[i]
            squadra2 = squadre[num_squadre - 1 - i]
            giornata.append((squadra1, squadra2))
        squadre.insert(1, squadre.pop())
        partite.append(giornata)
    return partite

# Funzione per leggere i giocatori da un file
def leggi_giocatori_da_file(nome_file):
    giocatori = []
    with open(nome_file, 'r') as file:
        righe = file.readlines()
        for riga in righe:
            riga = riga.strip()
            if not riga:
                continue
            nome_giocatore, abilità = riga.split(', ')
            giocatori.append({'nome': nome_giocatore, 'abilità': int(abilità)})
    return giocatori

# Funzione per creare le squadre
def crea_squadre(giocatori):
    num_squadre = len(giocatori) // 5
    giocatori = sorted(giocatori, key=lambda x: x['abilità'], reverse=True)
    squadre = [{'nome': f'Squadra{i}', 'punti': 0, 'giocatori': [], 'gol_fatti': 0, 'gol_subiti': 0, 'differenza_gol': 0} for i in range(num_squadre)]
    
    for i, giocatore in enumerate(giocatori):
        squadre[i % num_squadre]['giocatori'].append(giocatore)
    
    return squadre

# Funzione per aggiornare i punti delle squadre
def aggiorna_punti(squadra1, squadra2, risultato):
    gol1, gol2 = risultato
    squadra1['gol_fatti'] += gol1
    squadra1['gol_subiti'] += gol2
    squadra1['differenza_gol'] = squadra1['gol_fatti'] - squadra1['gol_subiti']
    squadra2['gol_fatti'] += gol2
    squadra2['gol_subiti'] += gol1
    squadra2['differenza_gol'] = squadra2['gol_fatti'] - squadra2['gol_subiti']
    
    if gol1 > gol2:
        squadra1['punti'] += 3
    elif gol1 < gol2:
        squadra2['punti'] += 3
    else:
        squadra1['punti'] += 1
        squadra2['punti'] += 1

# Funzione per salvare i risultati in una matrice
def salva_in_matrice(squadre_ordinate):
    matrice_risultati = []
    for squadra in squadre_ordinate:
        matrice_risultati.append([squadra['nome'], squadra['punti'], squadra['gol_fatti'], squadra['gol_subiti'], squadra['differenza_gol']])
    return matrice_risultati

# Funzione per salvare la classifica in un file
def salva_classifica(squadre, nome_file = 'classifica.txt'):
    squadre_ordinate = sorted(squadre, key=lambda x: (x['punti'], x['differenza_gol'], x['gol_fatti']), reverse=True)
    matrice_risultati = salva_in_matrice(squadre_ordinate)
    with open(nome_file, 'w') as file:
        file.write("-" * 36 + "\n")
        file.write(f"| {'Squadra':<10} {'Punti':<6} {'GF':<4} {'GS':<5} {'DG':<4}|\n")
        file.write("-" * 36 + "\n")
        count = 0
        for squadra in squadre_ordinate:
            file.write(f"| {matrice_risultati[count][0]:<10}| {matrice_risultati[count][1]:<4}| {matrice_risultati[count][2]:<4}| {matrice_risultati[count][3]:<4}| {matrice_risultati[count][4]:<3}|\n")
            file.write("-" * 36 + "\n")
            count += 1
        printskip("\nClassifica:")
        printskip("-" * 36)
        for i in range(len(matrice_risultati)):
            printskip(f"| {matrice_risultati[i][0]:<10}| {matrice_risultati[i][1]:<4}| {matrice_risultati[i][2]:<4}| {matrice_risultati[i][3]:<4}| {matrice_risultati[i][4]:<3}|")
            printskip("-" * 36)
    if risp=='no':
        input("Premi INVIO per continuare...")

# Funzione per salvare la classifica marcatori in un file
def salva_classifica_marcatori(marcatori, nome_file = 'classifica_marcatori.txt'):
    marcatori_ordinati = sorted(marcatori, key=lambda x: x[1], reverse=True)
    with open(nome_file, 'w') as file:
        file.write("-" * 35 + "\n")
        file.write(f"| {'Giocatore':<25} {'|Gol':<5} |\n")
        file.write("-" * 35 + "\n")
        for marcatore in marcatori_ordinati:
            file.write(f"| {marcatore[0]:<26}| {marcatore[1]:<4}|\n")
            file.write("-" * 35 + "\n")

# Funzione principale
def main():
    global risp
    #Vuoi saltare tutti i print?
    risp='si' #si o no
    
    os.system('clear' if os.name == 'posix' else 'cls')
    os.system('rm -rf classifica*' if os.name == 'posix' else 'del classifica*')
        
    nome_file_input = 'giocatori_input.txt'
    if not os.path.exists(nome_file_input):
        printskip(f"File di input non trovato. Generazione del file template: {nome_file_input}")
        genera_template(nome_file_input)
        printskip(f"File template generato: {nome_file_input}. Modifica il file con i nomi dei giocatori e le loro abilità.")
        return

    giocatori = leggi_giocatori_da_file(nome_file_input)
    if len(giocatori) % 10 != 0:
        printskip("Il numero di giocatori non è divisibile per 10. Aggiungi o rimuovi giocatori per avere un numero di squadre pari.")
        return

    squadre = crea_squadre(giocatori)
    giornate = genera_struttura_torneo(squadre)
    numero_giornata = 1
    marcatori = set()
    for giornata in giornate:
        printskip(f"\nGiornata {numero_giornata}")
        for squadra1, squadra2 in giornata:
            printskip(f"Partita: {squadra1['nome']} vs {squadra2['nome']}")
            partita_giocata = partita(squadra1['giocatori'], squadra2['giocatori'], marcatori)
            stampa_risultato(squadra1['nome'], squadra2['nome'], partita_giocata[0], partita_giocata[1])
            aggiorna_punti(squadra1, squadra2, partita_giocata)
        salva_classifica(squadre, f'classifica_giornata{numero_giornata}.txt')
        numero_giornata += 1
    salva_classifica_marcatori(marcatori)
    print('Finito')

if __name__ == "__main__":
    main()