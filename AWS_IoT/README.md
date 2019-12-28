# IOT EC2 and docker
###### Author: 余奇安 r07921010 電機所 碩二
## System architecture and objective:
Integrate PM2.5 sensor, Arduino, RPi to connect to AWS Iot service. Using MQTT protocol to communicate with AWS EC2 and store the PM2.5 value in mysql database which implemented by docker and manage by k8s.
![](https://i.imgur.com/nqU6tCI.png)

## Step 1
### Construct PM2.5 sensor to Ardunio and  transmit data to RPi
- Using UART(USB)
- Hareware construction ![](https://i.imgur.com/xkajTMR.png)
- The result of PM2.5 sensor on RPi ![](https://i.imgur.com/2FUQNq5.png)
- code PM25_LoraClientOK.ino `https://github.com/CheeAn-Yu/AIoT/blob/master/AWS_IoT/PM25_LoraClientOK.ino`




## Step 2
### Using RPi to push data to AWS IoT
- code `https://github.com/CheeAn-Yu/AIoT/blob/master/AWS_IoT/pm25.py`
- Run pm25.py on RPi
- Using MQTT protocol with topic Rpi/PM25
- Remeber to modify `policy securtiy` in AWS Iot service so that both publish and subscribe can be used.
    ```{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "iot:Publish",
            "iot:Receive"
          ],
          "Resource": [
            "arn:aws:iot:us-east-1:278900027829:topic/sdk/test/java",
            "arn:aws:iot:us-east-1:278900027829:topic/sdk/test/Python",
            "arn:aws:iot:us-east-1:278900027829:topic/Rpi/PM25",
            "arn:aws:iot:us-east-1:278900027829:topic/topic_2"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "iot:Subscribe"
          ],
          "Resource": [
            "arn:aws:iot:us-east-1:278900027829:topicfilter/sdk/test/java",
            "arn:aws:iot:us-east-1:278900027829:topicfilter/sdk/test/Python",
            "arn:aws:iot:us-east-1:278900027829:topicfilter/topic_1",
            "arn:aws:iot:us-east-1:278900027829:topicfilter/topic_2",
            "arn:aws:iot:us-east-1:278900027829:topicfilter/Rpi/PM25"
          ]
        },
        {
          "Effect": "Allow",
          "Action": [
            "iot:Connect"
          ],
          "Resource": [
            "arn:aws:iot:us-east-1:278900027829:client/sdk-java",
            "arn:aws:iot:us-east-1:278900027829:client/basicPubSub",
            "arn:aws:iot:us-east-1:278900027829:client/sdk-nodejs-*",
            "arn:aws:iot:us-east-1:278900027829:client/myRPi",
            "arn:aws:iot:us-east-1:278900027829:client/ec2"
          ]
        }
      ]
    }
    ```
- Testing ![](https://i.imgur.com/D689D2K.png) ![](https://i.imgur.com/QuMMWpD.png)

- Result ![](https://i.imgur.com/M5k4xCv.png)

## Step 3
### Subscribe data on EC2

- Need to install docker and mysql on EC2 machince first


### Using docker connect to mysql
- 下載mysql5.7鏡像 最新8.0
`sudo docker pull mysql:5.7`
 
- 绑定3306 port 並設定密碼
`sudo docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7`
-- 解釋
-e MYSQL_ROOT_PASSWORD=123456 : 初始化 root 用戶密碼,
- 執行docker內的 mysql
`sudo docker exec -it compassionate_nobel(container name) bash`
- 進入 mysql
`mysql -uroot -p123456`
- 遠端連接
`mysql -h172.17.0.2 -P3306 -uroot -p123456`
- 停止其他在運作的mysql
`sudo service mysql stop`
- 查看 container IP
`docker container inspect b0c420ef2913 (container id)| grep IP`
- Send file to ec2
`scp -i ~/Desktop/amazon.pem ~/Desktop/MS115.fa  ubuntu@ec2-54-166-128-20.compute-1.amazonaws.com:~/data/
- Download file from ec2
`scp -i ~/Desktop/amazon.pem ubuntu@ec2-54-166-128-20.compute-1.amazonaws.com:/data/ecoli_ref-5m-trim.fastq.gz ~/Download/``
- Connetct to mysql with python
`pip install mysql-connector-python`

```
# sample code
mydb = mysql.connector.connect(
      host="localhost",
      user="yusername",
      passwd="password",
      database="database_name"
)
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")    
mycursor.execute("SHOW TABLES")

mycursor.execute("INSERT INTO customers (name, address) VALUES ('John', 'Highway 21')")    
mydb.commit() # Use this command after insert or update

```
### create database in SQL
- `create database test` 創造新的database test
- ` use test` 進入test database

- 在test 建 pm25 表格
```
    Create table pm25(
    time char(100) not NULL,
    type char(20) not NULL,
    value char(20) not NULL,
    sequence char(20) primary key not NULL 
    );
```
- For this homework, I wrapped all sql management code in pm25_sub.py
- Run pm25_sub.py `https://github.com/CheeAn-Yu/AIoT/blob/master/AWS_IoT/pm25_sub.py`
- Result
    - We can see that PM2.5 value with timestamp was stored in mysql database.
    -   ![](https://i.imgur.com/uSJjgOU.png)

## Step 4
### Using K8s to manage docker container
- Open EC2 port fowarding 
- Choose Security Group ![](https://i.imgur.com/Seary4G.png)

- Choose Inbound ![](https://i.imgur.com/HQVuKXy.png)

- Connect to K8s `https://ec2-34-226-140-55.compute-1.amazonaws.com:4443/` domain_name(ec2-34-226-140-55.compute-1.amazonaws.com) + port(4443)

* Result ![](https://i.imgur.com/ZrL2Yit.png)
