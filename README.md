def con(query, values=[]):
    try:
        con = mysql.connect(
                host=host,
                port=port,
                user=user,
                database=database,
                password=password)
        cur = con.cursor()
        cur.execute(query,values)
        res=cur.fetchall()
       
        con.commit()
        if len(res)>0:
            return res
        return None
    finally:
        cur.close()
        con.close()
       
       
       
insert = """insert into HOLA (HOLA) values (%s)"""
select='select * from HOLA'
update="update HOLA set hola=%s where id=%s "
 
 
con(update,["Peronista",94])
res=con(select)
# print(res)
 
ancho_col=[0,0]
 
for hola in res:
    id=str(hola[0])
    hi=hola[1]
    if len(id) > ancho_col[0]:
        ancho_col[0]=len(id)
    if len(hi) > ancho_col[1]:  
        ancho_col[1]=len(hi)
 
# print("1"*8)
#
 
for i,r in enumerate(res):
   
    id =str(r[0])
    hi=r[1]
    diff_id= abs(len(id) - ancho_col[0])
    diff_hi=abs(len(hi) - ancho_col[1])
    if i == 0:
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+")
        print(("| HOLA"+" "*diff_hi)+"| "+("ID"+" "*diff_id+"|"))
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+")
 
    print("|"+(hi+(" "*diff_hi))+" | "+(id+(" "*diff_id)+"|"))
   
    if i == len(res)-1:
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+")
 
 https://sqlmodel.tiangolo.com/tutorial/
