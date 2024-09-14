#import tools #使用自訂module
import widget #使用自訂package

while True:
    cm = 0 #清除變數
    kg = 0 #清除變數

    #cm, kg = tools.input_data() #呼叫function #使用自訂module
    cm, kg = widget.input_data() #呼叫function #使用自訂package

    print(f'身高: {cm} 公分, 體重: {kg} 公斤')

    #BMI = tools.cal_bmi(kg=kg, cm=cm) #引數"名稱"的呼叫可以不依照順序 #使用自訂module
    BMI = widget.cal_bmi(kg=kg, cm=cm) #引數"名稱"的呼叫可以不依照順序 #使用自訂package

    print(f'BMI={BMI}')

    #print(tools.get_status(BMI)) #使用自訂module
    print(widget.get_status(BMI)) #使用自訂package

    paly_again = input("請問繼續嗎？(y/n)：")
    if paly_again == "n":
        break

print("程式結束")
