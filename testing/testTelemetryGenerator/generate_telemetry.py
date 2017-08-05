import csv
import math
import numpy as np
import random
import os
import string

def get_random_timestamps(start_time_seconds, end_time_seconds):
    min_time_step = 0.001 # 1KHz
    max_time_step = 1.0 # 1Hz

    random_time_step = random.triangular(min_time_step, max_time_step)
    return np.arange(start_time_seconds, end_time_seconds, random_time_step).tolist()

def create_dir_if_doesnt_exist(file_path):
    directory = os.path.dirname(file_path)

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

def generate_and_output_telemetry(channel_names, start_time_seconds, end_time_seconds, output_directory):
    
    create_dir_if_doesnt_exist(output_directory)

    channel_behaviors = ['sine', 'increase', 'decrease', 'on_off']

    min_value = -1000.0
    max_value = 1000.0
    min_ampl = 0.0001
    max_ampl = 10.0
    min_period = 0.01
    max_period = 20.0
    on_off_switch_probability = 0.001
    min_noise_percent = 0.00001
    max_noise_percent = 0.001
    min_phase_offset = 0
    max_phase_offset = math.pi

    filename = 'temp'

    mnemonic_channel_names = []

    with open(output_directory + filename, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile)

        for channel_name in channel_names:
            
            times = get_random_timestamps(start_time_seconds, end_time_seconds)

            channel_behavior = random.choice(channel_behaviors)
            # print channel_name, ':', channel_behavior

            if channel_behavior == 'sine':
                offset = random.triangular(min_value, max_value)
                ampl = random.triangular(min_ampl, max_ampl)
                phase_offset = random.triangular(min_phase_offset, max_phase_offset)
                noise_percent = random.triangular(min_noise_percent, max_noise_percent)
                period = random.triangular(min_period, max_period)

                values = [(offset + ampl * math.sin((2.0*math.pi/period) * time + phase_offset)) * (1.0 + random.triangular(min_noise_percent, max_noise_percent)) for time in times]

                mnemonic_channel_name = channel_name + 's'
            elif channel_behavior == 'increase':
                start_value = random.triangular(min_value, max_value, min_value + (max_value - min_value) / 8.0)
                end_value = random.triangular(start_value, max_value, start_value + (max_value - start_value) / 8.0)

                base_values = np.linspace(start_value, end_value, len(times))
                values = [value * (1.0 + random.triangular(min_noise_percent, max_noise_percent)) for value in base_values]

                mnemonic_channel_name = channel_name + 'i'
            elif channel_behavior == 'decrease':
                end_value = random.triangular(min_value, max_value, min_value + (max_value - min_value) / 8.0)
                start_value = random.triangular(end_value, max_value, end_value + (max_value - end_value) / 8.0)

                base_values = np.linspace(start_value, end_value, len(times))
                values = [value * (1.0 + random.triangular(min_noise_percent, max_noise_percent)) for value in base_values]

                mnemonic_channel_name = channel_name + 'd'
            elif channel_behavior == 'on_off':
                cur_state = random.choice([0, 1])
                values = []
                for i in range(len(times)):
                    values.append(cur_state)

                    if random.random() <= on_off_switch_probability:
                        # Switch occurred! Record next timestep
                        cur_state = 0 if (cur_state == 1) else 1
                mnemonic_channel_name = channel_name + 'o'
            else:
                print "Error: unspecified channel behavior \"%s\"" % channel_behavior
                print "Exiting early!"
                return

            # Now, the values list will contain all of our values, so let's write it to our csv
            for i, value in enumerate(values):
                csv_writer.writerow([mnemonic_channel_name, times[i], value])

            mnemonic_channel_names.append(mnemonic_channel_name)

    os.rename(output_directory + filename, output_directory + '_'.join(mnemonic_channel_names) + '.csv')


def get_channel_names(channel_name_base_file, channel_count):
    
    channel_name_base_strings = []

    with open(channel_name_base_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            channel_name = line.strip()
            if (channel_name not in channel_name_base_strings):
                channel_name_base_strings.append(channel_name)

    random.shuffle(channel_name_base_strings)

    channel_names = []

    while(len(channel_names) < channel_count):
        # Generate a random channel name
        random_channel_name = random.choice(channel_name_base_strings) + ''.join([random.choice(string.digits) for i in range(3)])
        if (random_channel_name) not in channel_names:
            channel_names.append(random_channel_name)

    return channel_names

def main():
    channel_count = 50
    start_time_seconds = 1000.0
    end_time_seconds = 2020.0
    channel_name_base_file = 'animal-words.txt'
    output_directory = os.getcwd() + '/output/channel_data/'
    channels_per_file = 4

    channel_names = get_channel_names(channel_name_base_file, channel_count)

    generated_channel_count = 0

    for i in range(len(channel_names))[::channels_per_file]:
        channel_name_subset = channel_names[i:i+channels_per_file]
        generate_and_output_telemetry(channel_name_subset, start_time_seconds, end_time_seconds, output_directory)

        generated_channel_count += channels_per_file
        if (generated_channel_count > channel_count):
            generated_channel_count = channel_count

        print "Generated %s files of %s" % (generated_channel_count, channel_count)


if __name__ == '__main__':
    main()