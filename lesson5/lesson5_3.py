def input_data():
    while True:
        try:
            cm = int(input("請輸入身高(公分):"))
            if cm > 300:
                raise Exception("超過300公分")
            break
        except ValueError:
            print("輸入格式錯誤")
            continue
        except Exception as e:
            print(f'輸入錯誤 {cm}')
            continue

    while True:
        try:
            kg = int(input("請輸入體重(公斤):"))
            if kg > 200:
                raise Exception("超過200公斤")
            break
        except ValueError:
            print("輸入格式錯誤")
            continue
        except Exception as e:
            print(f'輸入錯誤 {kg}')
            continue
    return (cm, kg)

while True:
    cm = 0
    kg = 0
    cm, kg = input_data()

    print(f'身高: {cm} 公分, 體重: {kg} 公斤')
    cm = (cm / 100) * (cm / 100)
    bmi = kg / cm
    print(f'BMI={bmi}')
    if bmi >= 35:
        print("過度肥胖")
    elif bmi >= 27:
        print("中度肥胖")
    elif bmi >= 24:
        print("適度肥胖")
    elif bmi >= 18.5:
        print("正常肥胖")
    else:
        print("體重過輕")

    paly_again = input("請問繼續嗎？(Y/N)：")
    if paly_again == "N":
        break

print("程式結束")
