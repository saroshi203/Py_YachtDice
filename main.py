# 족보는 닌텐도의 "세계 게임전집 51" 의 것을 사용함


# 리롤 기능 구상안:
# 딕셔너리에서 키를 이용하여 홀드/홀드 헤제할 다이스 선택
# 주사위 새로고침 기능 참조 하여 자동으로 판별할 수 있도록 함
# 값을 건너편 딕셔너리로 옮기고, 기존값을 0으로 설정
# 리롤 후 리롤 카운트 -1, 리롤 카운트가 0일경우 리롤 불가능
# 점수 입력 후 리롤 카운트 초기화

# 리롤 후에 손패랑 홀드 오름차순 정렬하기 < 가능하면

import random

# ● ┌ ─ ┐ │ └ ┘ 주사위 구성 텍스트
dice_art = {
   1: ("┌─────────┐",
       "│         │",
       "│    ●    │",
       "│         │",
       "└─────────┘"),
   2: ("┌─────────┐",
       "│  ●      │",
       "│         │",
       "│      ●  │",
       "└─────────┘"),
   3: ("┌─────────┐",
       "│  ●      │",
       "│    ●    │",
       "│      ●  │",
       "└─────────┘"),
   4: ("┌─────────┐",
       "│ ●     ● │",
       "│         │",
       "│ ●     ● │",
       "└─────────┘"),
   5: ("┌─────────┐",
       "│ ●     ● │",
       "│    ●    │",
       "│ ●     ● │",
       "└─────────┘"),
   6: ("┌─────────┐",
       "│ ●     ● │",
       "│ ●     ● │",
       "│ ●     ● │",
       "└─────────┘"),
}

dices = [] #현재 주사위 상황

hand_field = {1 : 0,
              2 : 0,
              3 : 0,
              4 : 0,
              5 : 0} #손패

hold_field = {1 : 0,
              2 : 0,
              3 : 0,
              4 : 0,
              5 : 0} #홀드

reroll_count = 2

score = [[0, True] for _ in range(12)] # [점수, 입력가능/불가능]
# 점수판 인덱스값
# 0:Aces | 1:Deuces | 2:Threes | 3:Fours | 4:Fives | 5:Sixs
# 6:Choice | 7:Four of a kind | 8:FullHouse | 9:S Straight | 10:L Straight | 11:Yacht


# --------------- 현재 주사위 새로고침 ---------------
#주사위에 변동이 있을경우 실행하여 dices 리스트 초기화및 반영

def dice_refresh(): 
    global dices
    dices.clear()
    for i in range (1,6):
       if hand_field[i] != 0:
          dices.append(hand_field[i])
       if hold_field[i] != 0:
          dices.append(hold_field[i])
    dices = sorted(dices)

# --------------- 주사위 굴리기 ---------------

def dice_roll(): 
    rolled = random.randint(1,6)
    return(rolled)

# --------------- 턴 첫번째 굴리기 ---------------
# 임시 리스트에 주사위 5개 굴리고 오름차순 정렬후 정렬된 값을 손패에 반영

def first_roll():
    global hand_field
    temp_dices = [dice_roll() for _ in range(5)]
    temp_dices.sort()
    for pos in range(1,6):
        hand_field[pos] = temp_dices[pos-1]
    dice_refresh()

# --------------- 리롤 및 정렬 ---------------

def reroll():
    pass

# --------------- 점수 계산식 ---------------

def Aces():
    return (dices.count(1)*1)

def Deuces():
    return (dices.count(2)*2)

def Threes():
    return (dices.count(3)*3)

def Fours():
    return (dices.count(4)*4)

def Fives():
    return (dices.count(5)*5)

def Sixs():
    return (dices.count(6)*6)



def Choice():
    return sum(dices)

def Four_of_a_kind():
    for i in set(dices): # 중복 제거한 각각 요소 검사
        if dices.count(i) >= 4: # 요소의 수가 4개 이상일 경우
            return sum(dices)
    return 0

def FullHouse():
    cnt = dices.count(dices[0]) # 주사위 리스트의 첫 값 카운팅
    if cnt == 3 and dices[3] == dices[4]: # 첫 값 3개가 같은 값 + 나머지 2개 값 같을 때
        return sum(dices)
    elif cnt == 2 and dices[2] == dices[3] == dices[4]:  # 첫 값 2개가 같은 값 + 나머지 3개 값 같을 때
        return sum(dices)
    else:
        return 0

def S_Straight():
    dice_set = set(dices)
    patterns = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
    for pattern in patterns:
        if pattern.issubset(dice_set): # a.issubset(b) 메서드는 a가 b안에 존재하는지 판별함
            return 15
    return 0

def L_Straight():
    dice_set = set(dices)
    if {1,2,3,4,5}.issubset(dice_set) or {2,3,4,5,6}.issubset(dice_set):
        return 30
    return 0

def Yacht():
    if len(set(dices))==1:
        return 50
    return 0
