from flask import Flask, jsonify, request
from flask import render_template
import dao;

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/findCountry')
def hello():
    country = dao.selectAll("select * from games", None)
    return jsonify(country)


@app.route('/findGames/<countryId>')
def findGames(countryId):
    games = dao.selectAll("select id,name from game_pirod gp where game_id=%s group by name", (countryId,))
    return jsonify(games)


@app.route('/findYears/<countryId>')
def findYear(countryId):
    games = dao.selectAll("select id,years from game_pirod where game_id=%s", (countryId,))

    return jsonify(games)


@app.route('/findTeam')
def findTeam():
    countryId = request.args.get('countryId')
    gameId = request.args.get('gameId')
    years = request.args.get('yearsStr')
    teams = []
    parameter=()
    sql="select t.id,t.name,p.`name`,g.country,p.years from team t left join game_pirod p on t.game_id=p.bsid left join games g on g.id=p.game_id where 1=1 and "
    if countryId != None:
        sql =sql +"g.id=%s"
        parameter=parameter+(countryId,)
    if gameId!=None:
        sql =sql +" and p.`name`=%s"
        parameter=parameter+(gameId,)
    if years!=None:
        sql =sql +" and p.`years`=%s"
        parameter=parameter+(years,)
    sql=sql+" group by t.id"
    teams=dao.selectAll(sql,parameter)
    return jsonify(teams)


@app.route('/query/<page>/<pageSize>', methods=["POST"])
def query(page, pageSize):
    page =int(page)-1
    fromData = int(pageSize) * int(page)
    limit = int(pageSize)
    begin = request.form['begin']
    end = request.form['end']

    firstTeam = request.form['firstTeam']
    secondTeam = request.form['secondTeam']
    queryData = []
    parameter = (firstTeam, secondTeam)
    dataSql = "SELECT d.bisai_id,DATE_FORMAT(d.bs_time,'%Y-%m-%d %H:%i'), (select name from team where id=d.first_team_id) as '主队'," \
              " (select name from team where id=d.second_team_id) as '客队', d.full_score, d.full_concede, d.full_bigsmall, d.half_score," \
              " d.half_concede, d.half_bigsmall, p.bocaiGs, p.first_zhudui, p.first_pankou, p.first_cidui, p.finally_zhudui, p.finally_pankou, p.finally_cidui,p.pankouName"
    fromSql = " FROM game_data d LEFT JOIN pankou p ON d.bisai_id = p.bisaiId WHERE " \
              "d.first_team_id = %s AND d.second_team_id = %s ";
    if begin != None and begin != '':
        fromSql = fromSql + " AND d.bs_time BETWEEN %s AND %s "
        parameter = parameter + (begin, end)
    fromSql = fromSql + " AND ( p.bocaiGs = '澳门' OR p.bocaiGs = '易胜博' ) ORDER BY d.bs_time DESC"
    countSql = "select count(d.bisai_id)" + fromSql
    total = dao.selectAll(countSql, parameter)
    dataSql = dataSql + fromSql + " limit %s,%s"
    parameter = parameter + (fromData, limit)
    queryData = dao.selectAll(dataSql, parameter)
    result = {"data": queryData, "total": total[0][0]}
    return jsonify(result)


if __name__ == '__main__':
    print(app.config.get('APPLICATION_ROOT'))
    app.run(debug=True, host='localhost', port=8089)
