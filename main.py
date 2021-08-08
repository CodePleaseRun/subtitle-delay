import sys
import os
import delay


def print_output(output):
    if output == 0:
        print(f'Subtitles delayed successfully.')
    else:
        print('Error in delaying subtitles.')


def main():
    if len(sys.argv) != 3:
        print('Usage: python main.py <srt file> <delay (in sec)>')
        quit()
    file_name = sys.argv[1]
    delay_time = sys.argv[2]

    if file_name == '.':
        for each_file in sorted(os.listdir()):
            if each_file.endswith('.srt'):
                output = delay.subs_delay(each_file, delay_time)
                print_output(output)
                break

    elif file_name == '*':
        for each_file in sorted(os.listdir()):
            if each_file.endswith('.srt'):
                output = delay.subs_delay(each_file, delay_time)
                print_output(output)
    else:
        output = delay.subs_delay(file_name, delay_time)
        print_output(output)


if __name__ == '__main__':
    main()
