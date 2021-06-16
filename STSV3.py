# todo:polar grid counter,add little random to each sat, exposurer time, measure convergence std vs mean, hit counter for multi strikes
# todo: statistics for different shells how many are above horizon and hits per shell -> name
#

from tqdm import tqdm
from random import randrange
import pyfiglet
import string
import os.path
import math
from datetime import datetime, timedelta
import ephem
import numpy as np
import sys
import pandas as pd
import os
import shutil
from datetime import date
import random
import statistics
import matplotlib.pyplot as plt



# set to True for plotting
plotting = True

step_size = 0.1
num_of_steps = 10
total_exposure = step_size * num_of_steps



result = pyfiglet.figlet_format("       TWILIGHT'S LAST GLEAMING    ", font="digital")
print(result)

result = pyfiglet.figlet_format("A SATILLITE SIMULATION SOFTWARE", font="digital")
print(result)

save_path = 'C:/Users/Taiko/Desktop/Starlink TLE/python_out'


def shell_gen(satname, sats, planes, alt, inc, day):
    nu = 3.9860044188 * (10 ** 14)

    day_of_year = str(int(day)).zfill(3)

    sats = int(sats)

    planes = int(planes)

    alt1=alt
    alt = (float(alt) + 6378.1371) * 1000

    period = math.sqrt(((alt ** 3) * (4 * math.pi ** 2)) / nu)

    mm = round(1 / period * 86400, 8)

    if len(str(mm)) < 11:
        mm = ' ' + str(mm)
    else:
        pass

    inc = float(inc)
    inc = str("{:.4f}".format(inc))

    out = satname+'_'+str(sats)+'_'+str(planes)+'_'+str(alt1)+'_'+str(round(float(inc), 2))+'.txt'

    if len(str(inc)) < 7:
        inc = '  ' + inc
    elif len(str(inc)) == 7:
        inc = ' ' + inc

    elif len(str(inc)) > 7:
        inc = inc

    y = np.linspace(0, 360, num=sats, endpoint=False)
    yy = np.linspace(0, 360, num=planes, endpoint=False)
    helpy = 1
    helpy2 = -1
    starlink_list = []
    random_number = random.uniform(0.01, 0.99)
    random_number = "{:.8f}".format(round(random_number, 8))
    random_number = str(random_number)
    random_number = random_number[1:]

    for i in range(int(sats * planes)):
        if i % sats == 0:
            helpy = 0
        else:
            helpy += 1

        if i % sats == 0 and i > 1:
            helpy2 += 1
        else:
            helpy2 += 0

        starlink_list.append(satname + '*' + str(i + 1))
        x = str(1) + ' ' + str(i + 1).zfill(5) + 'U 19029BR  21'+day_of_year + random_number + '  .00001103  00000-0  33518-4 0  999'

        x = x + str(checksum(x))

        starlink_list.append(fix_checksum(x))

        if len(str("{:.4f}".format(round(y[helpy], 4))).zfill(3)) < 7:
            var = '  ' + str("{:.4f}".format(round(y[helpy], 4))).zfill(3)

        elif len(str("{:.4f}".format(round(y[helpy], 4))).zfill(3)) < 8:
            var = ' ' + str("{:.4f}".format(round(y[helpy], 4))).zfill(3)
        else:
            var = str("{:.4f}".format(round(y[helpy], 4))).zfill(3)

        if len(str("{:.4f}".format(round(yy[helpy2], 4))).zfill(3)) < 7:
            bla = '  ' + str("{:.4f}".format(round(yy[helpy2], 4))).zfill(3)
        elif len(str("{:.4f}".format(round(yy[helpy2], 4))).zfill(3)) < 8:
            bla = ' ' + str("{:.4f}".format(round(yy[helpy2], 4))).zfill(3)

        else:
            bla = str("{:.4f}".format(round(yy[helpy2], 4))).zfill(3)
        xx = str(2) + ' ' + str(i + 1).zfill(5) + ' ' + inc + ' ' + bla + ' 0000001 299.7327 ' + var + ' ' + str(
            mm) + '  177'

        xx = xx + str(checksum(xx))

        starlink_list.append(fix_checksum(xx))

        completeName = os.path.join(save_path, out)

    with open(completeName, 'w') as f:
        for item in starlink_list:
            f.write("%s\n" % item)
    return starlink_list


def verify_checksum(*lines):
    """Verify the checksum of one or more TLE lines.

    Raises `ValueError` if any of the lines fails its checksum, and
    includes the failing line in the error message.

    """
    for line in lines:
        checksum = line[68:69]
        if not checksum.isdigit():
            continue
        checksum = int(checksum)
        computed = compute_checksum(line)
        if checksum != computed:
            complaint = ('TLE line gives its checksum as {}'
                         ' but in fact tallies to {}:\n{}')
            raise ValueError(complaint.format(checksum, computed, line))


def fix_checksum(line):
    """Return a new copy of the TLE `line`, with the correct checksum appended.

    This discards any existing checksum at the end of the line, if a
    checksum is already present.

    """
    return line[:68].ljust(68) + str(compute_checksum(line))


def compute_checksum(line):
    """Compute the TLE checksum for the given line."""
    return sum((int(c) if c.isdigit() else c == '-') for c in line[0:68]) % 10


def checksum(line):
    cksum = 0
    for i in range(len(line)):
        c = line[i]
        if c == ' ' or c == '.' or c == '+' or c in string.ascii_letters:
            continue
        elif c == '-':
            cksum = cksum + 1
        else:
            cksum = cksum + int(c)

    cksum %= 10

    return cksum


def time_diffrence(a, b):
    timea = datetime.strptime(a, "%H:%M")
    timeb = datetime.strptime(b, "%H:%M")
    return (timeb-timea).total_seconds()/60.0


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    if start < end:
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)

    else:
        delta = start - end
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return end + timedelta(seconds=random_second)
########################################################################################################################
# Set observer location


home = ephem.Observer()
locationKeyword = input(
    'Location keyword: ')  # type first few letters of the location keywords included in the entries below
locationName = ''

# --Observer() in Vienna, AUT ---------------
if locationKeyword.lower() == 'vienna'[0:len(locationKeyword)].lower():
    locationName = 'Vienna'
    print('Observer in Vienna')
    home = ephem.Observer()
    home.lon = '16.363449'  # +E
    home.lat = '48.210033'  # +N
    home.elevation = 0  # meters
    # home.temp = 26.0 #deg Celcius
    home.pressure = 0  # mbar
# ---------------------------------

# --Observer() at North Pole---------------
elif locationKeyword.lower() == 'north pole'[0:len(locationKeyword)].lower():
    locationName = 'North Pole'
    print('Observer at the North Pole')
    home = ephem.Observer()
    home.lon = '0.0'  # +E
    home.lat = '90.0'  # +N
    home.elevation = 0.0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() at South Pole---------------
elif locationKeyword.lower() == 'south pole'[0:len(locationKeyword)].lower():
    locationName = 'SouthPole'
    print('Observer at the South Pole')
    home = ephem.Observer()
    home.lon = '0.0'  # +E
    home.lat = '-90.0'  # +N
    home.elevation = 0.0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() in Tokyo, JPA---------------
elif locationKeyword.lower() == 'tokyo'[0:len(locationKeyword)].lower():
    locationName = 'Tokyo'
    print('Observer in Tokyo')
    home = ephem.Observer()
    home.lon = '139.83'  # +E
    home.lat = '35.65'  # +N
    home.elevation = 0.0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() in Pyongyang, DPRK ---------------
elif locationKeyword.lower() == 'pyongyang'[0:len(locationKeyword)].lower():
    locationName = 'Pyongyang, DPRK '
    print('Observer in Pyongyang')
    home = ephem.Observer()
    home.lon = '125.75'  # +E
    home.lat = '39.01'  # +N
    home.elevation = 0.0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------
# --Observer() in Steinbach, AUT---------------
elif locationKeyword.lower() == 'steinbach'[0:len(locationKeyword)].lower():
    locationName = 'Steinbach'
    print('Observer in Steinbach')
    home = ephem.Observer()
    home.lon = '13.549'  # +E
    home.lat = '47.83'  # +N
    home.elevation = 0.0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() in Tehran, IRA---------------
elif locationKeyword.lower() == 'theran'[0:len(locationKeyword)].lower():
    locationName = 'Tehran'
    print('Observer in Tehran')
    home = ephem.Observer()
    home.lon = '51.40'  # +E
    home.lat = '35.71'  # +N
    home.elevation = 1189  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() in Paranal, CHL---------------
elif locationKeyword.lower() == 'paranal'[0:len(locationKeyword)].lower():
    locationName = 'Paranal'
    print('Observer in Paranal')
    home = ephem.Observer()
    home.lon = '-70.4'  # +E
    home.lat = '-24.62'  # +N
    home.elevation = 1189  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------

# --Observer() in Cape Town, SA ---------------
elif locationKeyword.lower() == 'cape town'[0:len(locationKeyword)].lower():
    locationName = 'Cape Town'
    print('Observer in Cape Town')
    home = ephem.Observer()
    home.lon = '18.45'  # +E
    home.lat = '-34.27'  # +N
    home.elevation = 0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------
# --Observer() in Ushuaia, ARG ---------------
elif locationKeyword.lower() == 'ushuaia'[0:len(locationKeyword)].lower():
    locationName = 'Ushuaia'
    print('Observer in Ushuaia')
    home = ephem.Observer()
    home.lon = '-68.32'  # +E
    home.lat = '-54.80'  # +N
    home.elevation = 0  # meters
    home.date = datetime.utcnow()
    # home.temp = 26.0 #deg Celcius
    # home.pressure = 0.0 #mbar
# ---------------------------------
else:
    print('Location keyword not found.')
    sys.exit()

########################################################################################################################
# calculates from the  sq. degree a radius for the telescope with the same area
fov = input('What Field of View does the Telescope have in decimal Sq. Degrees?'
            '(1 arcmin = 0.016, 1 arcsec = 0.000277778): ')

fov = round(math.radians(math.sqrt(float(fov)/math.pi)), 2)
print(math.degrees(fov))
########################################################################################################################
artifical_stars = input('How many Targets should be generated?: ')

try:
    if float(artifical_stars):
        print(artifical_stars)
        artifical_stars = int(artifical_stars)

    else:
        artifical_stars = int(artifical_stars)
        sys.exit()

except ValueError:
    print('ERROR')
    sys.exit()

#######################################################################################################################
altitude = input('Till what Altitude should Stars and Starlink be simulated?: ')

try:
    if float(altitude):
        print(altitude)
        altitude = float(altitude)

    else:
        altitude = float(0.)

except ValueError:
    altitude = float(0.)

########################################################################################################################
iteration = input('How many iterations?: ')

try:
    if int(iteration):
        print(iteration)
        iteration = int(iteration)

    else:
        print('ERROR')
        sys.exit()

except ValueError:
    print('ERROR')
    sys.exit()
########################################################################################################################
twilight = str(input('What Twilight should be calculated?(civil,nautical,astronomical,night,dawnastro,dawnnautical'
                     'and dawncivil): '))
####################################################################################


for i in range(iteration):
    mag550 = 5.7
    extn = 0.12

    theta_plot = []
    r_plot = []

    theta_hit = []
    r_hit = []

    theta_sat = []
    r_sat = []

    MY_YEAR = datetime.now().year

    start_date = date(day=1, month=1, year=MY_YEAR).toordinal()
    end_date = date(day=31, month=12, year=MY_YEAR).toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    home.date = random_day
    ####################################################################################

    if twilight.lower() == 'civil'[0:len(twilight)].lower():
        home.horizon = '0.0'  # day end / civil dusk begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-6.0'  # civil dusk end / nautical dusk begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'nautical'[0:len(twilight)].lower():
        home.horizon = '-6.0'  # civil dusk end / nautical dusk begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-12.0'  # nautical dusk end / astronomical dusk begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'astronomical'[0:len(twilight)].lower():
        home.horizon = '-12.0'  # nautical dusk end / astronomical dusk begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-18.0'  # astronomical dusk end / night dusk begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'night'[0:len(twilight)].lower():
        home.horizon = '-18.0'  # astronomical dusk end / night begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-18.0'  # night end / astronomical dawn begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'dawnastro'[0:len(twilight)].lower():
        home.horizon = '-18.0'  # astronomical dusk end / night begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-12.0'  # night end / astronomical dawn begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'dawnnautical'[0:len(twilight)].lower():
        home.horizon = '-12.0'  # astronomical dusk end / night begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '-6.0'  # night end / astronomical dawn begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'dawncivil'[0:len(twilight)].lower():
        home.horizon = '-6.0'  # astronomical dusk end / night begin
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '0.0'  # night end / astronomical dawn begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    elif twilight.lower() == 'allnightlong'[0:len(twilight)].lower():
        home.horizon = '0.0'  # day end
        sun = ephem.Sun()
        d1 = datetime.strptime(str(home.next_setting(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
        home.horizon = '0.0'  # day begin
        sun = ephem.Sun()
        d2 = datetime.strptime(str(home.next_rising(sun, use_center=False)), "%Y/%m/%d %H:%M:%S")
    else:
        print('ERROR')
        sys.exit()
    sat_brig = []
    starlink_name = []
    star_name = []
    starlink_angle = []
    starlink_date = []
    duration = []
    intervall = []
    body_alt = []
    body_az = []
    velocity = []
    count_pre = 0
    sat_count_pre_lit = 0
    sat_count_pre_ecl = 0
    print(d1, d2)
    time = random_date(d1, d2)
    home.date = time
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    print(home.date)
    savedsatsnew = []

    folder = 'C:/Users/Taiko/Desktop/Starlink TLE/python_out'

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    day_of_year = time.timetuple().tm_yday
    #
    shell_gen('Starlink', 85, 84, 328, 30, day_of_year)
    shell_gen('Starlink', 85, 84, 334, 40, day_of_year)
    shell_gen('Starlink', 85, 84, 345, 53, day_of_year)
    shell_gen('Starlink', 100, 20, 373, 75, day_of_year)
    shell_gen('Starlink', 100, 40, 499, 53, day_of_year)
    shell_gen('Starlink', 12, 12, 604, 148, day_of_year)
    shell_gen('Starlink', 18, 18, 614, 116, day_of_year)
    shell_gen('Starlink', 50, 40, 360, 97, day_of_year)
    #
    shell_gen('OneWeb', 49, 36, 1200, 87.9, day_of_year)
    shell_gen('OneWeb', 72, 32, 1200, 40, day_of_year)
    shell_gen('OneWeb', 72, 32, 1200, 55, day_of_year)

    shell_gen('Kuiper System', 34, 34, 630, 51.9, day_of_year)
    shell_gen('Kuiper System', 36, 36, 610, 42, day_of_year)
    shell_gen('Kuiper System', 28, 28, 590, 33, day_of_year)

    shell_gen('Telesat', 12, 6, 1000, 99.5, day_of_year)
    shell_gen('Telesat', 13, 6, 1015, 98.98, day_of_year)
    shell_gen('Telesat', 13, 27, 1015, 98.98, day_of_year)

    shell_gen('Telesat', 9, 5, 1248, 37.4, day_of_year)
    shell_gen('Telesat', 11, 20, 1325, 50.88, day_of_year)
    shell_gen('Telesat', 33, 40, 1325, 50.88, day_of_year)

    shell_gen('GW-A59-1', 30, 16, 590, 85, day_of_year)
    shell_gen('GW-A59-2', 50, 40, 600, 50, day_of_year)
    shell_gen('GW-A59-3', 60, 60, 508, 55, day_of_year)

    shell_gen('GW-2-1', 36, 48, 1145, 30, day_of_year)
    shell_gen('GW-2-2', 36, 48, 1145, 40, day_of_year)
    shell_gen('GW-2-3', 36, 48, 1145, 50, day_of_year)
    shell_gen('GW-2-4', 36, 48, 1145, 60, day_of_year)

    path = 'C:/Users/Taiko/Desktop/Starlink TLE/python_out'
    files = os.listdir(path)
    completeName = os.path.join(save_path, "output_concatFile_new_radius.txt")

    with open(completeName, "w") as fo:
        for infile in files:
            with open(os.path.join(path, infile)) as fin:
                for line in fin:
                    fo.write(line)

    TLE_file2 = "C:/Users/Taiko/Desktop/Starlink TLE/python_out/output_concatFile_new_radius.txt"

    # load TLE data into python array
    with open(TLE_file2) as f:
        content2 = f.readlines()
        print(int(len(content2) / 3), 'TLEs loaded from starlinkTLE.txt.')
        for j in range(0, len(content2)):
            content2[j] = content2[j].replace('\n', '')  # remove endlines

    # read in each tle entry and save to list
    savedsats = []
    #satnames2 = []
    i_name2 = 0
    while 3 * i_name2 + 2 <= len(content2):
        # for each satellite in the content list...
        savedsats.append(ephem.readtle(content2[3 * i_name2], content2[3 * i_name2 + 1], content2[3 * i_name2 + 2]))
        #satnames2.append(content2[3 * i_name2])
        i_name2 += 1

    sat_altitude = 0
    error_counter = 0

    for sat in savedsats:
        try:
            home.date = time
            sat.compute(home)
            if math.degrees(sat.alt) > 0:

                savedsatsnew.append(sat)
                theta_sat.append(sat.az)
                r_sat.append(math.cos(sat.alt))
                delta = sat.range / 1000
                mag = mag550 + 5. * np.log10(delta / 550.) + extn * (1 / math.cos(sat.alt))
                sat_brig.append((12 - mag) ** 2)

            else:
                pass
        except RuntimeError:
            print('SOMETHING WENT WRONG')
            print(sat.name)
            error_counter += 1

    print((len(savedsatsnew)))

    stars_pre_selected = []
    stars = []
    RA = []
    DEC = []
    for n in range(artifical_stars):

        ra, dec = home.radec_of(az=random.uniform(0, 2 * math.pi),
                                alt=abs(math.asin(2 * random.random() - 1)))

        body = ephem.FixedBody()
        body._epoch = ephem.J2000
        body._ra = ephem.degrees(ra)
        body._dec = ephem.degrees(dec)

        body.compute(home)
        RA.append(ra)
        DEC.append(dec)

        if math.degrees(body.alt) > altitude:
            stars_pre_selected.append(body)
            count_pre += 1
        else:
            print(math.degrees(body.alt))
##############################################################################################

    star_num = 0
    hit_counter = 0
    for body in tqdm(stars_pre_selected):
        last_hit = ''
        star_num += 1
        if star_num % 500 == 0:
            print(round(hit_counter/star_num * 100, 2), '%')
        dt_10min = [time + timedelta(seconds=0.01 * x) for x in range(0, 6000 * 10)]
        dt_5min = [time + timedelta(seconds=0.01 * x) for x in range(0, 6000 * 5)]
        dt_1min = [time + timedelta(seconds=0.01 * x) for x in range(0, 100 * 1)]
        intervall = [dt_1min]
        body.compute(home)
        theta_plot.append(body.az)
        r_plot.append(math.cos(body.alt))

        if math.degrees(body.alt) > altitude:
            for dt in intervall:
                for obstime in dt:
                    home.date = obstime
                    body.compute(home)
                    for sat in savedsatsnew:
                        try:
                            sat.compute(home)
                            if math.degrees(sat.alt) > altitude:
                                angle = ephem.separation(sat, body)
                                if angle < fov:
                                    starlink_name.append(sat.name)
                                    if sat.name == last_hit:
                                        pass
                                    else:
                                        hit_counter += 1
                                        last_hit = sat.name


                                    star_name.append('Star ' + str(star_num))
                                    starlink_angle.append(angle)
                                    starlink_date.append(obstime)
                                    duration.append(len(dt)*0.05)
                                    body_az.append(body.az)
                                    body_alt.append(body.alt)
                                    delta = sat.range / 1000
                                    mag = mag550 + 5. * np.log10(delta / 550.) + extn * (1/math.cos(sat.alt))

                                    sat_elev = (float(sat.elevation) + 6378.1371 * 1000)
                                    vel = sat.range_velocity / 1000
                                    speed = math.sqrt((6.67 * 10 ** -11 * 5.972 * 10 ** 24) / sat_elev)
                                    velocity.append(speed/sat.elevation*57.29)

                                    # r_sat = float(sat.range / 1000)
                                    # umlaufzeit_sat = 2358720 * math.sqrt(r_sat ** 3 / 384000 ** 3)
                                    # omega = sat_elev * 2 * math.pi / vel
                                    # print(sat.range_velocity)
                                    # --- print the results of the hits live (note: this will effect performance)

                                    # print('Satellite height: ',  sat.elevation / 1000,'[km]')
                                    # print('Satellite brigthness: ', mag, '[mag]')
                                    # print('Satellite speed: ', speed / 1000, '[km/s]')
                                    # print('apparent angular velocity of the satellite: ', speed/sat.elevation*57.29,'[deg/s]')
                                    # print('Sat name: ', sat.name)
                                    # print('Star name: ', 'Star ' + str(star_num))
                                    # print('Seperation: ', angle,'[deg:min:sec]')
                                    # print('Exposure: ', len(dt)*0.05 , '[s]')
                                    # print('Star Coordinates', body.az, body.alt)
                                    # print('Time: ', obstime)
                                    # print('-------------------------------------------------------------------')

                                    theta_hit.append(body.az)
                                    r_hit.append(math.cos(body.alt))



                        except RuntimeError:
                            print('ERROR')
                            pass
        else:
            pass

    list_of_lists = list(zip(starlink_name, star_name, starlink_angle, starlink_date, duration, body_alt, body_az))
    df_o = pd.DataFrame(list_of_lists,
                      columns=['starlink_name', 'star_name', 'starlink_angle', 'starlink_date', 'duration',
                               'body_alt', 'body_az'])

    # analysis of the run
    df = (df_o.groupby(['starlink_name', 'star_name', 'duration'])['starlink_angle'].agg([('Min', 'min'), ('Max', 'max')])
          .add_prefix('test'))

    df2 = (df_o.groupby(['starlink_name', 'star_name'])['duration'].agg([('Min', 'min'), ('Max', 'max')])
           .add_prefix('duration'))

    grouped_df = df2.groupby(['starlink_name', 'star_name'])

    count = 0
    for key, item in grouped_df:
        a_group = grouped_df.get_group(key)
        count += 1
        #rint(a_group, "\n")

    #print(count)

    counts = pd.crosstab(index=[df_o["starlink_name"], df_o["star_name"]], columns=df_o["duration"])

    # Remove the name of the column array. It throws some people off to look at
    counts = counts.rename_axis(columns=None).reset_index()

    print( '0 sec '+ str(round((count * 100) / count_pre, 2)) + '% ' + 'Targets: ' ,count_pre,'Hits: ',count )
    print('mean_velocity: ' + str(statistics.mean(velocity)))
    print('mean_brigthness: ' , statistics.mean(sat_brig))

    # saving the data of the run
    df_o.to_csv("./" + str(twilight) + '_' + str(locationName) + '_' + str(round(math.degrees(fov), 2)) + '_' + str(altitude)
              + '_' + str(count_pre) + '_' + str(sat_count_pre_lit) + '_' + str(sat_count_pre_ecl) + '_'
              + str(timestamp) + ".csv", sep=',', index=False)

    # plotting the results
    if plotting:
        ax = plt.subplot(111, polar=True)

        title = str('UTC: ') + str(home.date)
        ax.set_title(title, va='bottom')
        plt.suptitle(locationName, fontsize=24, y=1)

        ax.set_theta_direction(-1)  # clockwise
        ax.set_theta_offset(np.pi / 2)  # put 0 degrees (north) at top of plot
        # ax.yaxis.set_ticklabels([])  # hide radial tick labels
        ax.grid(True)
        ax.scatter(theta_sat, r_sat, c='red', s=sat_brig)
        ax.scatter(theta_plot, r_plot, c='blue', s=2)
        ax.scatter(theta_hit, r_hit, c='black', s=15, marker="+")
        ax.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''])
        ax.set_yticklabels(['80', '60', '40', '20', '00'])
        plt.show()
    else:
        pass




