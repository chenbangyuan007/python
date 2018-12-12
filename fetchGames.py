import request
from pyquery import PyQuery as pq
import re
import dao
import time
def fetchGames(id,domain,years):
    id=str(id);
    url = 'http://info.win0168.com/cn/'+domain+'/'+years+'/'+id+'.html'
    html_doc = request.sendRequest(url)
    document = pq(html_doc)
    dataUrl=None
    version=time.strftime("%Y%m%d%H", time.localtime())
    if domain=='League' or domain =='SubLeague':
        script=document.find("script")
        # print(script)
        text=None
        for y in range(len(script)):
            value=pq(script[y]).text();
            if value.find("var SubSclassID")!=-1:
                text=value
                break
        SubSclassID = text.split(";")[6].split("=")[1].strip()
        print(SubSclassID)


        if(SubSclassID=='0'):
            dataUrl="http://info.win0168.com/jsData/matchResult/"+years+"/s"+id+".js?version="+version
        else:
            dataUrl="http://info.win0168.com/jsData/matchResult/"+years+"/s"+id+"_"+SubSclassID+".js?version="+version
    elif domain =='CupMatch':
         dataUrl="http://info.win0168.com/jsData/matchResult/"+years+"/c"+id+".js?version="+version


    print(dataUrl)
    data = request.sendRequest(dataUrl)
    teamStr=re.findall(r"var arrTeam =(.+?);",data)
    if len(teamStr)==0:
        return


    #球队
    print(teamStr[0])
    teams=eval(teamStr[0])
    for l in range(len(teams)):
        count=dao.selectOne("select count(id) from team where team_id=%s and game_id=%s",(teams[l][0],id))
        if count[0]>0:
            continue
        else:
            teamData=None
            if len(teams[l])==5:
                teamData=(teams[l][0],teams[l][1],teams[l][2],id)
                dao.insert("INSERT INTO team (team_id,name,alias,game_id) VALUES (%s,%s,%s,%s)",teamData)
            elif len(teams[l])==6:
                teamData=(teams[l][0],teams[l][1],teams[l][2],teams[l][5],id)
                dao.insert("INSERT INTO team (team_id,name,alias,image,game_id) VALUES (%s,%s,%s,%s,%s)",teamData)
            elif len(teams[l])>6:
                teamData=(teams[l][0],teams[l][1],teams[l][2],teams[l][5],teams[l][6],id)
                dao.insert("INSERT INTO team (team_id,name,alias,image,mark,game_id) VALUES (%s,%s,%s,%s,%s,%s)",teamData)

    #比赛数据
    gameDataStr=None
    if domain =='CupMatch':
        gameDataStr=re.findall(r"jh\[\"G.+\"\] =(.+?)\];\s",data)
    else:
        gameDataStr=re.findall(r"jh\[\"R_.+\"\] =(.+?)\];\s",data)
    lianSai = dao.selectOne("select name,game_id from game_pirod where bsid=%s limit 1", (id,))
    liansai=lianSai[0]
    country_id=lianSai[1]
    print(gameDataStr)
    for j in range(len(gameDataStr)):
        gameDataStr[j]=gameDataStr[j]+']'
        try:
            per = eval(gameDataStr[j])
            for i in range(len(per)):
                data=per[i];
                if '<br/>' in data[3]:
                    date=data[3].split('<br/>')
                    data[3]=years+'-'+date[0]+' '+date[1]
                gameData=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]
                          ,data[9],data[10],data[11],data[12],data[13],j+1,years,liansai,country_id)
                print(gameData)
                count=dao.selectOne("select count(id) from game_data where bisai_id=%s and game_id=%s",(data[0],id))
                if count[0]>0:
                    updateData=(data[6],data[7],data[8]
                                ,data[9],data[10],data[11],data[12],data[13],years,liansai,country_id,data[0],id)
                    dao.insert("UPDATE game_data set full_score=%s,half_score=%s,first_sort=%s,second_sort=%s,full_concede=%s "
                               ",half_concede=%s,full_bigsmall=%s,half_bigsmall=%s,years=%s,liansai=%s,country_id=%s where bisai_id=%s and game_id=%s",updateData)
                else:
                    dao.insert("INSERT INTO game_data (bisai_id,game_id,mark,bs_time,first_team_id,second_team_id,full_score, "
                               "half_score,first_sort,second_sort,full_concede,half_concede,full_bigsmall,half_bigsmall,turn,years,liansai,country_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%,%)",gameData)
        except Exception:
            dataStr=''
            if gameDataStr[j].endswith("]]]"):
                gamePer=re.findall(r"\[{1,2}(.+?)\]\]",gameDataStr[j])
                for j in range(len(gamePer)):
                    dataStr=dataStr+gamePer[j]+']'
            else:
                dataStr=gameDataStr[j]
            per=re.findall(r"\[{1,2}(.+?)\]{1,2}",dataStr)
            for i in range(len(per)):
                data=per[i].replace("\'","").split(",")
                if len(data)<13:
                    continue
                if '<br/>' in data[3]:
                    date=data[3].split('<br/>')
                    data[3]=years.split('-')[0]+'-'+date[0]+' '+date[1]
                gameData=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]
                                    ,data[9],data[10],data[11],data[12],data[13],j+1,years,liansai,country_id)
                print(gameData)
                count=dao.selectOne("select count(id) from game_data where bisai_id=%s and game_id=%s",(data[0],id))
                if count[0]>0:
                    updateData=(data[6],data[7],data[8]
                                ,data[9],data[10],data[11],data[12],data[13],years,liansai,country_id,data[0],id)
                    dao.insert("UPDATE game_data set full_score=%s,half_score=%s,first_sort=%s,second_sort=%s,full_concede=%s "
                               ",half_concede=%s,full_bigsmall=%s,half_bigsmall=%s,years=%s,,liansai=%s,country_id=%s where bisai_id=%s and game_id=%s",updateData)
                else:
                    dao.insert("INSERT INTO game_data (bisai_id,game_id,mark,bs_time,first_team_id,second_team_id,full_score, "
                           "half_score,first_sort,second_sort,full_concede,half_concede,full_bigsmall,half_bigsmall,turn,years,liansai,country_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",gameData)


if __name__=="__main__":
    fetchGames(75,"CupMatch","2018")



