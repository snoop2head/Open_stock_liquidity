from flask import Flask, render_template, jsonify, request
from app_pandas_to_google_spreadsheet import write_on_gs
from app_pandas_to_dataframe_or_to_excel import error_detector

app = Flask(__name__)


## 설명서를 주는 부분 = HTML

@app.route('/')
def register():
   return render_template('register.html')

## 데이터를 주고받는 부분 = API

## making dictionary from received id and password
## checking input data, matching with registered data
## API
@app.route('/datareceive', methods=['POST'])
def generator():
    id_receive = request.form['id_give']
    print("클라가 입력한 종목명: " + id_receive)
    if error_detector(id_receive) == "endgame":
        return jsonify({'result': 'fail'})
    else:
        write_on_gs(id_receive)
        return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

