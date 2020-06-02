# Flask_in_mongoDB


- 가상환경 설치하기
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
- requirements.txt 설치

```
pip install -r requirements.txt
```
- flask 실행

```
py main.py
```

- mongoDB 
```
mongoimport -d movie --collection movie_info --file D:/teample/movies_info_super_final.csv --type csv --headerline
```
## DB table

- movie_info : movies_info_super_final.csv
- users_review : users_super_final.csv --> DB명 수정할 계획[user_info]
- movie_info_keyword : movies_info_kw_setting_v3.csv