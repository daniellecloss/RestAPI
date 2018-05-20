from flask import Flask
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

app = Flask(__name__)
api = Api(app)

mysql = MySQL()

mysql.init_app(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = cfg['mysql']['MysqlDatabaseUser']
app.config['MYSQL_DATABASE_PASSWORD'] = cfg['mysql']['MysqlDatabasePassword']
app.config['MYSQL_DATABASE_DB'] = cfg['mysql']['MysqlDatabaseDb']
app.config['MYSQL_DATABASE_HOST'] = cfg['mysql']['MysqlDatabaseHost']


class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email',
                                type=str, help='Email address to create user')
            parser.add_argument('password',
                                type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser', (_userEmail, _userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode': '200',
                        'Message': 'User creation success'}
            else:
                return {'StatusCode': '1000', 'Message': str(data[0])}
            cursor.close()
            conn.close()

        except Exception as e:
            return {'error': str(e)}


api.add_resource(CreateUser, '/CreateUser')

if __name__ == '__main__':
    app.run(debug=True)
