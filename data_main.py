import dao;
import fetchGames
import  fechPankou
import time
game_id=None
def runFetchALL(bsid):
    allgames=dao.selectAll("select id from games",None)
    for i in range(len(allgames)):
        pirod=None
        if bsid >0:
            pirod=dao.selectAll("select years,bsid,lv,lv1 from game_pirod where game_id=%s and bsid>=%s order by bsid asc",(allgames[i][0],bsid))
        else:
            pirod=dao.selectAll("select years,bsid,lv,lv1 from game_pirod where game_id=%s order by bsid asc",(allgames[i][0],))
        for j in range(len(pirod)):
            year=pirod[j][0]
            game_id=pirod[j][1]
            lv=pirod[j][2]
            lv1=pirod[j][3]
            domine=None
            if lv==1 and lv1==0:
                domine='League'
            elif lv==1 and lv1==1:
                domine='SubLeague'
            elif lv==2 and lv1==0:
                domine='CupMatch'
            print(game_id,domine,year)
            fetchGames.fetchGames(game_id,domine,year)
            time.sleep(1)


def runFetchNotFetched():
    sql="select p.years,p.bsid,p.lv,p.lv1,count(d.id) from game_pirod p left join game_data d on p.bsid=d.game_id group by p.bsid,p.years HAVING count(d.id)=0"
    allgames=dao.selectAll(sql,None)
    for i in range(len(allgames)):
        year=allgames[i][0]
        game_id=allgames[i][1]
        lv=allgames[i][2]
        lv1=allgames[i][3]
        domine=None
        if lv==1 and lv1==0:
            domine='League'
        elif lv==1 and lv1==1:
            domine='SubLeague'
        elif lv==2 and (lv1==0 or lv1==1):
            domine='CupMatch'
        print(game_id,domine,year)
        fetchGames.fetchGames(game_id,domine,year)
        time.sleep(1)


def runFetchPankou():
    sql="select g.bisai_id from game_data g left join pankou p on p.bisaiId=g.bisai_id where g.error=0  GROUP BY g.bisai_id HAVING count(p.id)=0 or count(p.id)=1 "
    allgames=dao.selectAll(sql,None)
    for i in range(len(allgames)):
        id=allgames[i][0]
        try:
            fechPankou.fetchPankou(id)
        except:
            dao.insert("Update game_data set error=1 where bisai_id=%s",(id,))

def fechRecentBisai(y):
    sql ="select years,bsid,lv,lv1 from game_pirod p  where p.years like '"+y+"%'"
    pirod=dao.selectAll(sql,None)
    for j in range(len(pirod)):
        year=pirod[j][0]
        game_id=pirod[j][1]
        lv=pirod[j][2]
        lv1=pirod[j][3]
        domine=None
        if lv==1 and lv1==0:
            domine='League'
        elif lv==1 and lv1==1:
            domine='SubLeague'
        elif lv==2 and lv1==0:
            domine='CupMatch'
        print(game_id,domine,year)
        fetchGames.fetchGames(game_id,domine,year)
        time.sleep(1)

def fechRecentPankou(year):
    sql ="select d.bisai_id from game_pirod p left join game_data d on d.bisai_id=p.bsid where p.years like '"+year+"%' and d.bisai_id is not null"
    pirod=dao.selectAll(sql,None)
    for i in range(len(pirod)):
        id=pirod[i][0]
        try:
            fechPankou.fetchPankou(id)
        except:
            continue



if __name__=="__main__":
    # fechRecentBisai("2018")
    runFetchPankou()
    # runFetchNotFetched()
    # games.fechCountry()
    # try:
    #     runFetchALL(0)
    # except:
    #     if game_id!=None:
    #         runFetchALL(game_id)

