def input_data()->tuple[int, int]:
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
    return cm, kg

def get_status(bmi:float)->str:
    if bmi >= 35:
        return "過度肥胖(BMI≧35)"
    elif bmi >= 27:
        return "中度肥胖(BMI≧27)"
    elif bmi >= 24:
        return "適度肥胖(BMI≧24)"
    elif bmi >= 18.5:
        return "正常肥胖"
    else:
        return "體重過輕"

def cal_bmi(cm:int, kg:int) -> float:
    cm = (cm / 100) * (cm / 100)
    bmi = kg / cm
    return bmi
