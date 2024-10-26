
from kanji_lists import JLPT
import random,pygame



def Game(diff):
    # we give the difficulty and topic that was given as an argument
    if isinstance(diff,int):
        topic="グッドラック.txt"
    else:
        if diff=='Lebron James':
            topic='Lebron_James.txt'
        elif diff=='日本料理':
            topic='日本料理.txt'
        else:
            topic='北海度.txt'
        diff=random.choice([1,2,3,4,5])

    if diff==1:
        lis=JLPT.TANOS.N1
    elif diff==2:
        lis=JLPT.TANOS.N2
    elif diff==3:
        lis=JLPT.TANOS.N3
    elif diff==4:
        lis=JLPT.TANOS.N4
    elif diff==5:
        lis=JLPT.TANOS.N5
    
    
    x=[] 
    for k in lis:
        x.append(k)


    # select the file chosen and shuffle the content in a list

    sentences=[]
    with open(topic)as file:
        for line in file:
            line=line.strip()
            sentences.append(line)
    
    random.shuffle(sentences)

    # we find a sentence with a kanji in the list created before
    # we keep a record of the sentence and kanji to guess 
    for sentence in sentences:
        for kanji in x:
            answer=''
            if kanji in sentence and len(sentence)<125:
                place=sentence.find(kanji)
                question=sentence.replace(sentence[place]," ○ ")
                answer=kanji        
                break
        if answer!='':
            break

        
    # we create a list of random kanji wich does not contain same answer to show the user multiple choices 
    wrong=[]
    wrong.append(answer)
    l=0          
    while l<3:
        random.shuffle(x)
        if x[0] not in wrong:
            wrong.append(x[0])
            l+=1
    random.shuffle(wrong)

    
    # create a dictionary of all possible choices
    choices={}
    num=0
    for ans in wrong:
        num+=1
        choices[num]=ans 

    round=(question,choices,answer,diff)
    return round


def login(username):
    
    if len(username)<3:
        return False
    else:
        with open("user.txt") as file:
            data=file.read().split("\n")
            data_names=[]
            for item in data:
                names=''
                for cara in item:
                    if cara==',':
                        break
                    names+=cara
                data_names.append(names)
            for name in data_names:
                if username == name:
                    return True
            return False



def register(username):
    
    username_taken=login(username)
    if username_taken==True:
        return False
    
    if len(username)<3:
        return False
    else:
        str = f"\n{username},0,N1:0,N2:0,N3:0,N4:0,N5:0"
        with open("user.txt","a") as file:
            file.write(str)
            
        return True

        

def command():
    li_str=[
        '',
        'Difficulty choice',
        'Topic choice',
        'Leaderboard',
    ]
    licommand=[(number,li_str[number]) for number in range(1,4)]
    return licommand

    
def difficulty_level():
    li_diff=[
    '',
    'JLPT N1',
    'JLPT N2',
    'JLPT N3',
    'JLPT N4',
    'JLPT N5',
    ]
    lidifficulty=[(number,li_diff[number]) for number in range(1,len(li_diff))]
    def trie(item):
        item[0]
    lidifficulty.sort(key=trie(lidifficulty), reverse=True)
    return lidifficulty


def stats(username,points,level):
    with open("user.txt") as file:
        data=file.read().split("\n")
    with open("user.txt","w") as file_w:
        len_max=len(data)
        count=0
        for item in data:
            count+=1
            item=item.split(',')
            if item[0]==username:
                item[1]=str(int(item[1])+int(points))
                if level==1:
                    item[2]=int(item[2][-1])+points
                    item[2]=f'N1:{str(item[2])}'
                elif level==2:
                    item[3]=int(item[3][-1])+points
                    item[3]=f'N2:{str(item[3])}'
                elif level==3:
                    item[4]=int(item[4][-1])+points
                    item[4]=f'N3:{str(item[4])}'
                elif level==4:
                    item[5]=int(item[5][-1])+points
                    item[5]=f'N4:{str(item[5])}'
                elif level==5:
                    item[6]=int(item[6][-1])+points
                    item[6]=f'N5:{str(item[6])}'
            item=','.join(item)
            
            if count!=len_max:
                item+='\n'
            file_w.write(item)
        

def leaderboard():
    with open("user.txt")as file:
        data=file.read().split('\n')
        def trie(item): 
            item=item.split(',')
            return int(item[1])
        lb=sorted(data, key=trie, reverse=True)
        return lb

            
def initialize_game():
    pygame.init()
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font("fonts/Gen Shin Gothic Monospace Bold.ttf", 40)
    game_font2 = pygame.font.Font("fonts/Gen Shin Gothic Monospace Bold.ttf", 24)
    game_font3 = pygame.font.Font("fonts/Gen Shin Gothic Monospace Bold.ttf", 16)
    points=0
    round=0
    list_question_done=[]

    def word_wrap(text,choices,answer,number):
        window.fill((63, 71, 143))
        list_sentences=[]
        count=0
        end=25
        while True:
            str='   '
            for words in text[end-25:end]:
                count+=1
                str+=words
            end+=25
            list_sentences.append(str)
            if count>=len(text):
                break  
    
        height_sentences=20
        for sentences in list_sentences:
            text_question=game_font2.render(sentences, True, (255, 255, 255))
            window.blit(text_question, (0,height_sentences))
            height_sentences+=40
        width_choice=60
        for choice in choices:
            str=f'{choice}: {choices[choice]}'
            text_choice=game_font2.render(str, True, (255, 255, 255))
            window.blit(text_choice, (width_choice,270))
            width_choice+=150
            
        if number==0:
            str_answer='Make a choice between 1-4'
            text_answer=game_font2.render(str_answer, True, (255, 255, 255))
            window.blit(text_answer, (320-text_answer.get_width()/2,400))
        elif number!=0:
            if choices[number]==answer:
                str_answer=f'正解!'
                text_answer=game_font.render(str_answer, True, (0, 255, 0))
                window.blit(text_answer, (320-text_answer.get_width()/2,350))
            else:
                str_answer=f'不正解!'
                text_answer=game_font.render(str_answer, True, (255, 0, 0))
                window.blit(text_answer, (320-text_answer.get_width()/2,350))
            real_answer=f'The answer was: {answer}'
            text_real_answer= game_font2.render(real_answer, True, (255, 255, 255))
            window.blit(text_real_answer, (320-text_real_answer.get_width()/2,400))
                
           


    Main_menu=True
    Access=True             #all 3 true at the begining of the game 
    auth_valid=True

    AccessMenu=False
    login_loop=False
    first_register=False
    difficulty_key=False
    rank_key=False
    topic_key=False
    game_key=False
    end_game_key=False
    answer_screen=False
    next_round_key=False
    while True:

        
        if Main_menu==True:
            window.fill((63, 71, 143))
            text = game_font.render("漢字を学ぼう!", True, (255, 255, 255))
            text2 = game_font2.render("Log in", True, (255, 255, 255))
            text3 = game_font2.render("Register", True, (255, 255, 255))
            login_butt=pygame.draw.rect(window, (36, 42, 99), (320-(text2.get_width()+80)/2, 300, text2.get_width()+80, text2.get_height()+40))
            register_butt=pygame.draw.rect(window, (36, 42, 99), (320-(text3.get_width()+80)/2, 380, text3.get_width()+80, text3.get_height()+40))
            username=''

            window.blit(text, (320-text.get_width()/2,240-text.get_height()))
            window.blit(text2,(320-text2.get_width()/2,320))
            window.blit(text3,(320-text3.get_width()/2,400))

        
        if login_loop==True:
            window.fill((63, 71, 143))
            
            text_sqr=pygame.draw.rect(window, (36, 42, 99), (200, 240, 230, 50))
            return_butt=pygame.draw.rect(window, (36, 42, 99), (500, 400, 100, 50))
            text = game_font.render("Enter username:", True, (255, 255, 255))
            text_return = game_font2.render("Return", True, (255, 255, 255))
            log_in_surface=game_font2.render(username,True,(255,255,255))

            window.blit(text, (320-text.get_width()/2,200-text.get_height()))
            window.blit(text_return, (515,405))
            window.blit(log_in_surface,(210,245))

            if auth_valid==False:
                text2 = game_font2.render("Invalid username", True, (255, 0, 0))
                window.blit(text2, (320-text2.get_width()/2,300))
        

        if login_loop == False and AccessMenu==True:
            Access=False
            window.fill((63, 71, 143))
            commands=command()
            height=100
            text=game_font.render("Main Menu", True, (255, 255, 255))
            window.blit(text, (320-text.get_width()/2,10))
            for com in commands:
                c=game_font2.render(f'{com[0]:15} : {com[1]}',True,(255,255,255) )
                window.blit(c,(0,height))
                height+=50       
            if difficulty_key==True:
                diff_choice=difficulty_level()
                width_lev=25
                for level in diff_choice:
                    pygame.draw.rect(window, (36, 42, 99), (width_lev-10, 290, 110, 50))
                    jlpt_=game_font3.render(f'{level[0]} : {level[1]}',True,(255,255,255) )
                    window.blit(jlpt_,(width_lev,300))
                    width_lev+=125
                diff_expld=game_font2.render(f'Easy {'>'*20} Hard',True,(255,255,255) )
                window.blit(diff_expld,(320-diff_expld.get_width()/2,380))
            if topic_key==True:
                topic_choice=['1:Lebron James','2:日本料理','3:北海度']
                width_topic=0
                for topic in topic_choice:
                    pygame.draw.rect(window, (36, 42, 99), (150+width_topic, 290, 120, 50))
                    choice=game_font3.render(topic,True,(255,255,255) )
                    window.blit(choice,(210-(choice.get_width()/2)+width_topic,300))
                    width_topic+=135
            if rank_key==True:
                leaders=leaderboard()
                height_player=270
                pygame.draw.rect(window,(36, 42, 99),(20,270,600,200))
                ranking=1
                for leader in leaders[0:3]:
                    leader=leader.split(',')
                    player=game_font2.render(f'{ranking:15} {leader[0]} : {leader[1]} total points',True,(255,255,255) )
                    player_stats=game_font3.render(f'{'correct answers:':>35} {leader[2]}|{leader[3]}|{leader[4]}|{leader[5]}|{leader[6]}',True,(255,255,255) )
                    window.blit(player,(0,height_player))
                    window.blit(player_stats,(0,height_player+30))
                    height_player+=65
                    ranking+=1
            

        if game_key==True:
            word_wrap(question,choices,answer,number)            
        if answer_screen==True:
            word_wrap(question,choices,answer,number)
          
        if next_round_key==True:
            press_space= game_font3.render("Press Space ", True, (255, 255, 255))
            window.blit(press_space,(620-press_space.get_width(),440))
        
        if end_game_key==True:
            window.fill((63, 71, 143))
            list_score=["Score",f"{points}/5"]
            height_score=100
            for line in list_score:
                text_score = game_font.render(line, True, (255, 255, 255))
                window.blit(text_score,(320-text_score.get_width()/2,height_score))
                height_score+=80
            try_again = game_font2.render("Try Again", True, (255, 255, 255))
            quit= game_font2.render("QUIT", True, (255, 255, 255))
            try_again_butt=pygame.draw.rect(window, (36, 42, 99), (320-(try_again.get_width()+80)/2, 300, try_again.get_width()+80, try_again.get_height()+40))
            quit_butt=pygame.draw.rect(window, (36, 42, 99), (320-(quit.get_width()+80)/2, 380, quit.get_width()+80, quit.get_height()+40))
            window.blit(try_again,(320-try_again.get_width()/2,320))
            window.blit(quit,(320-quit.get_width()/2,400))

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # mouse events for main menu and login in   
            if event.type == pygame.MOUSEBUTTONDOWN and Access==True:
                if login_loop==True:
                    if return_butt.collidepoint(pygame.mouse.get_pos()):
                        auth_valid=True
                        first_register=False
                        login_loop=False
                        Main_menu=True               
                elif login_butt.collidepoint(pygame.mouse.get_pos()):
                    login_loop=True
                    Main_menu=False             
                elif register_butt.collidepoint(pygame.mouse.get_pos()):
                    login_loop=True
                    first_register=True
                    Main_menu=False    
            
            if event.type == pygame.KEYDOWN:
                # loging in and menu
                if login_loop == True:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif len(username)<15 and event.key != pygame.K_RETURN:
                        username+= event.unicode
                    if event.key == pygame.K_RETURN and first_register==True:
                        auth_valid=register(username)
                        if auth_valid==True:
                            AccessMenu=True
                            login_loop=False
                            Access=False
                    elif event.key == pygame.K_RETURN:
                        auth_valid=login(username)
                        if auth_valid==True:
                            AccessMenu=True
                            login_loop=False
                            Access=False
                
                if AccessMenu==True:
                    if event.key==pygame.K_5 and difficulty_key==True:
                        next_round_key=True
                        difficulty_key=False
                        diff_lev=5
                    if event.key==pygame.K_4 and difficulty_key==True:
                        next_round_key=True
                        difficulty_key=False
                        diff_lev=4
                    if event.key==pygame.K_3 and difficulty_key==True:
                        next_round_key=True
                        difficulty_key=False
                        diff_lev=3
                    elif event.key==pygame.K_3 and topic_key==True:
                        next_round_key=True
                        topic_key=False
                        diff_lev='北海度'
                    elif event.key==pygame.K_3:
                        rank_key=True
                        difficulty_key=False
                        topic_key=False
                    if event.key==pygame.K_2 and topic_key==True:
                        next_round_key=True
                        topic_key=False
                        diff_lev='日本料理'
                    elif event.key==pygame.K_2 and difficulty_key==False:
                        topic_key=True
                        difficulty_key=False
                        rank_key=False
                    elif event.key==pygame.K_2 and difficulty_key==True:
                        next_round_key=True
                        difficulty_key=False
                        diff_lev=2
                    if event.key==pygame.K_1 and difficulty_key==True:
                        next_round_key=True
                        difficulty_key=False
                        diff_lev=1
                    elif event.key==pygame.K_1 and topic_key==False:
                        difficulty_key=True
                        rank_key=False
                        topic_key=False
                    elif event.key==pygame.K_1 and topic_key==True:
                        next_round_key=True
                        topic_key=False
                        diff_lev='Lebron James'
                
                # Game buttons
                if end_game_key==False and next_round_key==True and event.key==pygame.K_SPACE:
                    if round==5:
                        next_round_key=False
                        end_game_key=True
                        answer_screen=False
                        stats(username,points,diff_stats)               
                    else:
                        AccessMenu=False
                        next_round_key=False
                        game_key=True
                        game_data=Game(diff_lev)
                        question=game_data[0]
                        choices=game_data[1]
                        answer=game_data[2]
                        diff_stats=game_data[3]
                        number=0
                        while True:
                            try:
                                if question in list_question_done:
                                    game_data=Game(diff_lev)
                                    question=game_data[0]
                                    choices=game_data[1]
                                    answer=game_data[2]
                                else:
                                    break 
                            except: 
                                raise ValueError('Lack of sentences')
                                
                                
                        list_question_done.append(question)

                if game_key==True and event.key == pygame.K_1:
                    if answer==choices[1]:
                        points+=1
                    number=1
                    round+=1
                    game_key=False
                    answer_screen=True
                    next_round_key=True
                    
                if game_key==True and event.key == pygame.K_2:
                    if answer==choices[2]:
                        points+=1
                    number=2
                    round+=1
                    game_key=False
                    answer_screen=True
                    next_round_key=True

                if game_key==True and event.key == pygame.K_3:
                    if answer==choices[3]:
                        points+=1
                    number=3
                    round+=1
                    game_key=False
                    answer_screen=True
                    next_round_key=True
                    
                if game_key==True and event.key == pygame.K_4:
                    if answer==choices[4]:
                        points+=1
                    number=4
                    round+=1
                    game_key=False
                    answer_screen=True
                    next_round_key=True
                    
            # mouse events for end of game   
            if event.type == pygame.MOUSEBUTTONDOWN and end_game_key==True:   
                if try_again_butt.collidepoint(pygame.mouse.get_pos()): 
                    round=0
                    points=0
                    end_game_key=False
                    AccessMenu=True    
                if quit_butt.collidepoint(pygame.mouse.get_pos()):
                    exit()

        
        pygame.display.flip()

        clock.tick(60)




if __name__=="__main__":
    initialize_game()