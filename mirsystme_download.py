from urllib.request import urlopen
import pandas as pd
import sys

def clean_query(lQuery):
    
    lQ = []
    for query in lQuery:
        s = query

        for i in ["{","}","[","]"]:
            s = s.replace(i,"")

        lQ.append(eval(s))

    df = pd.DataFrame(lQ)
    
    return df


def query_mir_mirsystem(mir):
    #Get HTML
    url = "http://mirsystem.cgm.ntu.edu.tw/miRNA2Target_genelist.php?id=104&mi=%s&GO=0&tier=tier2&KEGG=0&Biocarta=0&PID=0&Reactome=0&validation=1&hit=1"%mir
    response = urlopen(url)
    html = response.read().decode('utf-8')
    #Explit Result
    lQuery = html.split("{\"cell\":")[1:-1]
    #Col Name
    colNames = ['Target Gene', 'Gene Description', 'Validation', 'DIANA', 'miRanda', 'miRBridge', 'PicTar', 'PITA', 'rna22', 'TargetScan', 'Total hit']
    lTarget = ['Validation', 'DIANA', 'miRanda', 'miRBridge', 'PicTar', 'PITA', 'rna22', 'TargetScan']
    #Clean string
    df = clean_query(lQuery)
    if not df.empty:
        df.columns = colNames
        df["miRNA"] = mir
        df[lTarget] = df[lTarget].replace("V",1)
        df[lTarget] = df[lTarget].replace("",0)

    return df

def main():
    mir = sys.argv[1]
    df = query_mir_mirsystem(mir)
    df.to_csv("mirsystem_table_%s.tsv"%mir, sep = "\t")
    

if __name__ == "__main__":
    main()
