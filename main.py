# 족보는 닌텐도의 "세계 게임전집 51" 의 것을 사용함

# 커멘드 등은 터미널 내에서 특정 커멘드 숫자를 입력받으면 해당 커멘드가 실행되도록 "텍스트 게임" 형식으로 진행. 
# 게임 화면 예시

# (1번 주사위) (2번 주사위) (3번 주사위) (4번 주사위) (5번 주사위) 
# (홀드되었을경우 초록색으로 색 변경하기)

# ==================== [ 1 / 12 턴 시작 ] ====================

# [ 1st Roll 결과 ]

# ==================================================
#                   << 점수판 >>
# ==================================================
# --- 상단 섹션 (Upper Section) --------------------
# [101] Aces(1)      |     0점 | (점수가 입력 가능할경우엔 초록색으로 점수 표시)
# [102] Deuces(2)    |     0점 | (점수가 입력 불가능하다면 커멘드 번호를 빨간색으로 표시.)
# [103] Threes(3)    |     0점 | (족보가 완성되지 않아 점수가 0인 경우 빨간색 대신 노란색으로 표시. 이 경우 값의 입력은 가능하며 0이 점수로 입력됨)
# [104] Fours(4)     |     0점 | 
# [105] Fives(5)     |     0점 |
# [106] Sixs(6)      |     0점 |
# --------------------------------------------------
#   상단 섹션 합계: 0점 | 보너스 (63점 이상 시 35점): 0점
# --------------------------------------------------
# --- 하단 섹션 (Lower Section) --------------------
# [201] Choice       |     0점 | 
# [202] 4 of a Kind  |     0점 |
# [203] Full House   |     0점 |
# [204] S.Straight   |     0점 | 
# [205] L.Straight   |     0점 |
# [206] Yacht        |     0점 |
# ==================================================
# 총: 0점
# ==================================================
#
# [301] Hold | [401] Reroll 

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

dices = [] #현재 주사위 상황 표시용 리스트 (게임시 겉으로 표시되는 값)

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

roll_count = 0

score = [[0, True] for _ in range(12)] # [점수, 입력가능/불가능]
# 점수판 인덱스값
# 0:Aces | 1:Deuces | 2:Threes | 3:Fours | 4:Fives | 5:Sixs
# 6:Choice | 7:Four of a kind | 8:FullHouse | 9:S Straight | 10:L Straight | 11:Yacht

# 커멘드 값
# [101] Aces | [102] Deuces | [103] Threes | [104] Fours | [105] Fives | [106] Sixs
# [201] Choice | [202] Four of a kind | [203] FullHouse | [204] S Straight | [205] L Straight | [206] Yacht
#
# [301] Hold 
# [401] Reroll 


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
    global roll_count
    temp_dices = [dice_roll() for _ in range(5)]
    temp_dices.sort()
    for pos in range(1,6):
        hand_field[pos] = temp_dices[pos-1]
    roll_count += 1
    dice_refresh()

# --------------- 홀드 ---------------

def hold():
    global hand_field, hold_field
    
    # 인덱스 입력받기
    user_input = input("홀드/해제할 주사위 인덱스 입력 (1~5, 쉼표로 구분): ")
    
    # 입력값 파싱
    try:
        indices = [int(x.strip()) for x in user_input.split(',')]
    except ValueError:
        print("올바른 숫자를 입력해주세요.")
        return False
    
    # 입력값 검증: 1~5 사이의 값인지
    for idx in indices:
        if idx < 1 or idx > 5:
            print(f"잘못된 인덱스: {idx}. 1~5 사이의 값을 입력해주세요.")
            return False
    
    # 입력값 검증: 중복된 값이 없는지
    if len(indices) != len(set(indices)):
        print("중복된 인덱스가 있습니다.")
        return False
    
    # 각 인덱스에 대해 홀드/홀드해제 수행
    for idx in indices:
        # 자동으로 홀드인지 홀드 해제인지 판별
        if hand_field[idx] != 0:  # 손패에 값이 있으면 -> 홀드
            hold_field[idx] = hand_field[idx]
            hand_field[idx] = 0
            print(f"인덱스 {idx}: 홀드됨 (값: {hold_field[idx]})")
        elif hold_field[idx] != 0:  # 홀드에 값이 있으면 -> 홀드 해제
            hand_field[idx] = hold_field[idx]
            hold_field[idx] = 0
            print(f"인덱스 {idx}: 홀드 해제됨 (값: {hand_field[idx]})")
        else:
            print(f"인덱스 {idx}: 해당 위치에 주사위가 없습니다.")
    
    # 홀드/홀드 해제 시에는 정렬하지 않음 (구상안대로)
    dice_refresh()
    return True

# --------------- 리롤 및 정렬 ---------------

def _sort_field(field_dict):
    """정렬 시 같은 인덱스 중복을 막기 위해 기존 점유 인덱스 안에서만 값 정렬"""
    filled_indices = sorted(idx for idx, value in field_dict.items() if value != 0)
    sorted_values = sorted(field_dict[idx] for idx in filled_indices)
    for idx in field_dict.keys():
        field_dict[idx] = 0
    for idx, value in zip(filled_indices, sorted_values):
        field_dict[idx] = value


def reroll():
    global roll_count, hand_field

    if roll_count >= 3:
        print("리롤 횟수를 모두 사용했습니다.")
        return False

    reroll_targets = [idx for idx, value in hand_field.items() if value != 0]
    if not reroll_targets:
        print("손패에 리롤할 주사위가 없습니다.")
        return False

    for idx in reroll_targets:
        hand_field[idx] = dice_roll()

    roll_count += 1

    _sort_field(hand_field)
    _sort_field(hold_field)
    dice_refresh()
    return True


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

# --------------- 점수 계산 함수 매핑 ---------------

score_functions = {
    0: Aces,
    1: Deuces,
    2: Threes,
    3: Fours,
    4: Fives,
    5: Sixs,
    6: Choice,
    7: Four_of_a_kind,
    8: FullHouse,
    9: S_Straight,
    10: L_Straight,
    11: Yacht
}

# --------------- 색상 코드 ---------------

class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'

# --------------- 주사위 출력 ---------------

def print_dices():
    """주사위를 ASCII 아트로 출력"""
    print("\n" + "=" * 60)
    
    # 각 위치(1~5)의 주사위 값 가져오기
    dice_values = []
    held_status = []
    for pos in range(1, 6):
        if hold_field[pos] != 0:
            dice_values.append(hold_field[pos])
            held_status.append(True)
        elif hand_field[pos] != 0:
            dice_values.append(hand_field[pos])
            held_status.append(False)
        else:
            dice_values.append(0)
            held_status.append(False)
    
    # 주사위 번호 출력
    header = "    "
    for i in range(5):
        status = f"{Colors.GREEN}[HOLD]{Colors.RESET}" if held_status[i] else "      "
        header += f"  [{i+1}]{status}   "
    print(header)
    
    # 주사위 ASCII 아트 출력 (5줄)
    for line in range(5):
        row = "    "
        for i in range(5):
            if dice_values[i] != 0:
                color = Colors.GREEN if held_status[i] else Colors.RESET
                row += color + dice_art[dice_values[i]][line] + Colors.RESET + "  "
            else:
                row += "             "
        print(row)
    
    print("=" * 60)

# --------------- 점수판 출력 ---------------

def print_scoreboard():
    """점수판 출력"""
    score_names_upper = ["Aces(1)", "Deuces(2)", "Threes(3)", "Fours(4)", "Fives(5)", "Sixs(6)"]
    score_names_lower = ["Choice", "4 of a Kind", "Full House", "S.Straight", "L.Straight", "Yacht"]
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}                   << 점수판 >>{Colors.RESET}")
    print("=" * 60)
    print("--- 상단 섹션 (Upper Section) --------------------")
    
    # 상단 섹션 (101~106)
    for i in range(6):
        cmd_num = 101 + i
        name = score_names_upper[i]
        
        if not score[i][1]:  # 이미 입력된 점수
            print(f" {Colors.RED}[{cmd_num}]{Colors.RESET} {name:<12} | {score[i][0]:>5}점 | (입력완료)")
        else:  # 입력 가능
            potential_score = score_functions[i]()
            if potential_score > 0:
                print(f" {Colors.GREEN}[{cmd_num}] {name:<12} | {potential_score:>5}점 | (입력가능){Colors.RESET}")
            else:
                print(f" {Colors.YELLOW}[{cmd_num}] {name:<12} | {potential_score:>5}점 | (0점 입력){Colors.RESET}")
    
    # 상단 섹션 합계 및 보너스
    upper_sum = sum(score[i][0] for i in range(6))
    bonus = 35 if upper_sum >= 63 else 0
    print("-" * 50)
    print(f"  상단 섹션 합계: {upper_sum}점 | 보너스 (63점 이상 시 35점): {bonus}점")
    print("-" * 50)
    
    print("--- 하단 섹션 (Lower Section) --------------------")
    
    # 하단 섹션 (201~206)
    for i in range(6):
        cmd_num = 201 + i
        score_idx = 6 + i
        name = score_names_lower[i]
        
        if not score[score_idx][1]:  # 이미 입력된 점수
            print(f" {Colors.RED}[{cmd_num}]{Colors.RESET} {name:<12} | {score[score_idx][0]:>5}점 | (입력완료)")
        else:  # 입력 가능
            potential_score = score_functions[score_idx]()
            if potential_score > 0:
                print(f" {Colors.GREEN}[{cmd_num}] {name:<12} | {potential_score:>5}점 | (입력가능){Colors.RESET}")
            else:
                print(f" {Colors.YELLOW}[{cmd_num}] {name:<12} | {potential_score:>5}점 | (0점 입력){Colors.RESET}")
    
    # 총점
    lower_sum = sum(score[i][0] for i in range(6, 12))
    total = upper_sum + bonus + lower_sum
    print("=" * 60)
    print(f"{Colors.BOLD}총점: {total}점{Colors.RESET}")
    print("=" * 60)

# --------------- 커맨드 메뉴 출력 ---------------

def print_commands(roll_count):
    """사용 가능한 커맨드 출력"""
    print(f"\n{Colors.CYAN}[ 리롤 횟수: {roll_count}/3 ]{Colors.RESET}")
    print("-" * 40)
    if roll_count < 3:
        print(f"[301] 홀드 설정/해제\n[401] 리롤")
    else:
        print(f"[301] 홀드 설정/해제  |  {Colors.RED}[401] 리롤 (횟수 소진){Colors.RESET}")
    print("[101~106] 상단 섹션에 점수 입력")
    print("[201~206] 하단 섹션에 점수 입력")
    print("-" * 40)

# --------------- 점수 입력 ---------------

def enter_score(cmd):
    """점수 입력 처리"""
    global score
    
    # 커맨드 번호를 점수 인덱스로 변환
    if 101 <= cmd <= 106:
        score_idx = cmd - 101
    elif 201 <= cmd <= 206:
        score_idx = cmd - 201 + 6
    else:
        print("잘못된 커맨드입니다.")
        return False
    
    # 이미 입력된 점수인지 확인
    if not score[score_idx][1]:
        print("이미 점수가 입력된 항목입니다.")
        return False
    
    # 점수 계산 및 입력
    calculated_score = score_functions[score_idx]()
    score[score_idx][0] = calculated_score
    score[score_idx][1] = False
    
    score_names = ["Aces", "Deuces", "Threes", "Fours", "Fives", "Sixs",
                   "Choice", "4 of a Kind", "Full House", "S.Straight", "L.Straight", "Yacht"]
    print(f"\n{Colors.GREEN}✓ {score_names[score_idx]}에 {calculated_score}점이 입력되었습니다!{Colors.RESET}")
    return True

# --------------- 턴 초기화 ---------------

def reset_turn():
    """턴 시작 시 손패와 홀드 초기화"""
    global hand_field, hold_field, roll_count, dices
    hand_field = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    hold_field = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    roll_count = 0
    dices = []

# --------------- 게임 초기화 ---------------

def reset_game():
    """게임 전체 초기화"""
    global score
    score = [[0, True] for _ in range(12)]
    reset_turn()

# --------------- 최종 결과 출력 ---------------

def print_final_result():
    """게임 종료 시 최종 결과 출력"""
    score_names_upper = ["Aces(1)", "Deuces(2)", "Threes(3)", "Fours(4)", "Fives(5)", "Sixs(6)"]
    score_names_lower = ["Choice", "4 of a Kind", "Full House", "S.Straight", "L.Straight", "Yacht"]
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.CYAN}            🎲 최종 게임 결과 🎲{Colors.RESET}")
    print("=" * 60)
    
    print("\n--- 상단 섹션 ---")
    for i in range(6):
        print(f"  {score_names_upper[i]:<12}: {score[i][0]:>3}점")
    
    upper_sum = sum(score[i][0] for i in range(6))
    bonus = 35 if upper_sum >= 63 else 0
    print(f"  {'소계':<12}: {upper_sum:>3}점")
    print(f"  {'보너스':<12}: {bonus:>3}점 {'(63점 달성!)' if bonus > 0 else ''}")
    
    print("\n--- 하단 섹션 ---")
    for i in range(6):
        print(f"  {score_names_lower[i]:<12}: {score[6+i][0]:>3}점")
    
    lower_sum = sum(score[i][0] for i in range(6, 12))
    total = upper_sum + bonus + lower_sum
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.GREEN}  최종 점수: {total}점{Colors.RESET}")
    print("=" * 60)
    
    # 간단한 평가
    if total >= 250:
        print(f"{Colors.GREEN}🏆 훌륭합니다! 최고의 요트 플레이어!{Colors.RESET}")
    elif total >= 200:
        print(f"{Colors.CYAN}👍 좋은 점수입니다!{Colors.RESET}")
    elif total >= 150:
        print(f"{Colors.YELLOW}😊 괜찮은 게임이었습니다.{Colors.RESET}")
    else:
        print(f"💪 다음엔 더 좋은 결과가 있을 거예요!")

# --------------- 메인 게임 루프 ---------------

def main():
    """메인 게임 함수"""
    reset_game()
    
    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}{Colors.CYAN}        🎲 요트 다이스 (Yacht Dice) 🎲{Colors.RESET}")
    print("=" * 60)
    print("  닌텐도 '세계 게임전집 51' 기반 요트 다이스")
    print("  12턴 동안 최고의 점수를 노려보세요!")
    print("=" * 60)
    
    input("\n엔터를 눌러 게임을 시작하세요...")
    
    # 12턴 진행
    for turn in range(1, 13):
        reset_turn()
        
        print("\n" + "=" * 60)
        print(f"{Colors.BOLD}{Colors.BLUE}        ========== [ {turn} / 12 턴 시작 ] =========={Colors.RESET}")
        print("=" * 60)
        
        # 첫 번째 굴리기
        input("\n엔터를 눌러 주사위를 굴리세요...")
        first_roll()
        
        turn_complete = False
        
        while not turn_complete:
            # 현재 상태 출력
            print(f"\n{Colors.CYAN}[ {roll_count}번째 Roll 결과 ]{Colors.RESET}")
            print_dices()
            print_scoreboard()
            print_commands(roll_count)
            
            # 커맨드 입력
            try:
                cmd = input("\n> ").strip()
                if not cmd:
                    continue
                cmd = int(cmd)
            except ValueError:
                print(f"{Colors.RED}숫자를 입력해주세요.{Colors.RESET}")
                continue
            
            # 커맨드 처리
            if cmd == 301:  # 홀드
                hold()
            elif cmd == 401:  # 리롤
                if roll_count >= 3:
                    print(f"{Colors.RED}리롤 횟수를 모두 사용했습니다. 점수를 입력해주세요.{Colors.RESET}")
                else:
                    reroll()
            elif 101 <= cmd <= 106 or 201 <= cmd <= 206:  # 점수 입력
                if enter_score(cmd):
                    turn_complete = True
            else:
                print(f"{Colors.RED}잘못된 커맨드입니다. (101~106, 201~206, 301, 401){Colors.RESET}")
    
    # 게임 종료
    print_final_result()
    
    # 재시작 옵션
    while True:
        restart = input("\n다시 플레이하시겠습니까? (y/n): ").strip().lower()
        if restart == 'y':
            main()
            break
        elif restart == 'n':
            print("\n게임을 종료합니다. 감사합니다! 🎲")
            break
        else:
            print("y 또는 n을 입력해주세요.")

# --------------- 게임 실행 ---------------

if __name__ == "__main__":
    main()
