import random

score = 0
all_equasions = []

def generate_easy():
    symbols = ['+', '-', '*']
    equasion_to_print = f'{random.randint(2, 9)} {random.choice(symbols)} {random.randint(2, 9)}'
    equasion = equasion_to_print.split() 
    
    if '+' in equasion:
        answer = int(equasion[0]) + int(equasion[2])
    
    if '-' in equasion:
        answer = int(equasion[0]) - int(equasion[2])
    
    if '*' in equasion:
        answer = int(equasion[0]) * int(equasion[2])
    return equasion_to_print, answer

def generate_hard():
    number = random.randint(11, 29)
    answer = number ** 2
    return number, answer

def how_much_tasks(count, type):
    if type == 'easy':
        for i in range(count):
            all_equasions.append(generate_easy())
    
    if type == 'hard':
        for i in range(count):
            all_equasions.append(generate_hard())
    
def game():
    global score
    for i in all_equasions:
        print(i[0])
        while True:
            guess = input()
            if guess.strip('-').isdigit():
                if int(guess) == i[1]:
                    print('Right!')
                    score += 1
                    break
                else:
                    print('Wrong!')
                    break
            else:
                print('Wrong format! Try again.')

def savefile(name, score, level):
    file_save = open('results.txt', 'a')
    if level == 'easy':
        file_save.write(f'{name}: {score} in level 1 (simple operations with numbers 2-9).')
    if level == 'hard':
        file_save.write(f'{name}: {score} in level 2 (integral squares 11-29).')
    file_save.close()


def main():
    level = None
    
    while True:
        which_level = int(input('Which level do you want? Enter a number:\n1 - simple operations with numbers 2-9\n2 - integral squares of 11-29'))
        
        if which_level == 1:
            how_much_tasks(5, 'easy')
            level = 'easy'
            game()
            break
        
        if which_level == 2:
            how_much_tasks(5, 'hard')
            level = 'hard'
            game()
            break
        else:
            print('Incorrect format.')
    save = input(f'Your mark is {score}/5. Would you like to save the result? Enter yes or no.')
    
    if save in ['yes', 'YES', 'y', 'Yes']:
        name = input('What is your name?')
        savefile(name, f'{score}/5', level)
        print('The results are saved in "results.txt".')

main()
