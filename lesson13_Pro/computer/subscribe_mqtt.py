import paho.mqtt.client as mqtt #需安裝pip install paho-mqtt
import os, csv
from datetime import datetime 
import sqlite3
from sqlite3 import Error

def insert_to_sqlite(values):
    try:
        #db_root_dir = os.getcwd()
        #db_root_dir = os.path.join(db_root_dir, 'pico.db')
        #filename = db_root_dir + "pico.db"
        conn = sqlite3.connect('./data/pico.db')
    except Exception as e:
        print (e)
        return
    
    sql = """
    INSERT INTO chicken_accommodation (record_date, equipment, value) VALUES (
    ?,?,?)
    """

    myCursor =  conn.cursor()
    myCursor.execute(sql, values)
    conn.commit()
    myCursor.close()
    conn.close()

def record(topic:str, value:int | float):
    '''
    #檢查是否有data資料夾,沒有就建立data資料夾
    #取得今天日期,如果沒有今天日期.csv,就建立一個全新的今天日期.csv
    #將參數r的資料,儲存進入csv檔案內
    #parameters date:str -> 這是日期
    #parameters topic:str -> 這是訂閱的topic
    #parameters value:int -> 這是訂閱的value
    '''

    root_dir = os.getcwd()
    data_dir = os.path.join(root_dir, 'data')

    #目錄不存在則建立目錄
    if not os.path.isdir(data_dir):
        os.mkdir('data')

    today = datetime.today()
    current_dt_str = today.strftime("%Y-%m-%d %H:%M:%S")
    date = today.strftime("%Y-%m-%d")
    filename = date + ".csv"

    #get file arbspath
    full_path = os.path.join(data_dir, filename)

    if not os.path.exists(full_path):
        #如沒有檔案則建立檔案
        with open(full_path, mode='w', encoding='utf-8', newline='') as file:
            file.write('時間,設備,值\n')

    with open(full_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_dt_str, topic, value])
        insert_to_sqlite((current_dt_str, topic, float(value)))

def on_connect(client, userdata, flags, reason_code, properties):
    #連線bloker成功時，只會執行一次
    client.subscribe("SA-12/#")
    
def on_message(client, userdata, msg):
    global led_origin_value
    global temperature_origin_value
    global light_origin_status

    topic = msg.topic
    value = msg.payload.decode()

    if topic == "SA-12/LED_LV":
        led_value = int(value)
        if led_value != led_origin_value:
            led_origin_value = led_value
            print(f'led_value: {led_value}')
            record(topic, led_value)

    if topic == "SA-12/TEMPERATURE":
        temperature_value = float(value)
        if temperature_origin_value != temperature_value:
            temperature_origin_value = temperature_value
            print(f'temperature_value: {temperature_value}')
            record(topic, temperature_value)
    
    if topic == "SA-12/LIGHT_SWITCH":
        light_status = int(value)
        if light_origin_status != light_status:
            light_origin_status = light_status
            print(f'light_status: {light_status}')
            record(topic, light_status)


    #print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

def main():
    client = mqtt.Client(callback_api_version = mqtt.CallbackAPIVersion.VERSION2)
    #設定用戶名稱密碼
    username = "pi"
    password = "raspberry"
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.0.252", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    led_origin_value = 0
    temperature_origin_value = 0.0
    light_origin_status = 0
    main()
                     
                    