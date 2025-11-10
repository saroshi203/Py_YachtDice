# 족보는 닌텐도의 "세계 게임전집 51" 의 것을 사용함

# git이 아직 별로 안익숙해져서 함수 추가한거 반영시키고 하는 과정에서 제강님이 커밋한거 로그 실수로 지워버렸어요 :(

# 리롤 기능 구상안:
# 딕셔너리에서 키를 이용하여 홀드/홀드 헤제할 다이스 선택
# 주사위 새로고침 기능 참조 하여 자동으로 판별할 수 있도록 함
# 값을 건너편 딕셔너리로 옮기고, 기존값을 0으로 설정
# 리롤 후 리롤 카운트 -1, 리롤 카운트가 0일경우 리롤 불가능
# 점수 입력 후 리롤 카운트 초기화

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

#현재 주사위 상황 새로고침
#주사위에 변동이 있을경우 실행하여 dices 리스트 초기화및 반영
def dices_now(): 
    global dices
    dices.clear()
    for i in range (1,6):
       if hand_field[i] != 0:
          dices.append(hand_field[i])
       if hold_field[i] != 0:
          dices.append(hold_field[i])
    dices = sorted(dices)

# 주사위 굴리기
def dice_roll(): 
    rolled = random.randint(1,6)
    return(rolled)

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
    pass

def L_Straight():
    pass

def Yacht():
    if len(set(dices))==1:
        return 50
    else:
        return 0

