import matplotlib.pyplot as plt

wid = 5

msg_cnt = [4, 10, 25, 50, 75, 100]
msg_cnt2 = [i + wid for i in msg_cnt]

sign_time = [0.0694, 0.1315, 0.3014, 0.6194, 1.0031, 1.1913]
ver_time = [0.0787, 0.1450, 0.3172, 0.6212, 0.9681, 1.200]

plt.figure(figsize=(10, 9))
plt.rc('font', size=16)          # controls default text sizes
plt.rc('axes', labelsize=28)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=22)    # legend fontsize

# plt.ticklabel_format(style='plain')
# plt.ylim(0, 0.8)

plt.xticks(msg_cnt)
plt.xlabel("Number of Aggregate Messages")
plt.bar(msg_cnt, sign_time, color='g', width=wid, label='Aggregate message signing')
# plt.plot(msg_cnt, sign_time, 'bo')

plt.ylabel("Time (seconds)")
# plt.plot(msg_cnt, ver_time, 'ro')

plt.legend()
plt.show()

#########################

plt.figure(figsize=(10, 9))
plt.rc('font', size=16)          # controls default text sizes
plt.rc('axes', labelsize=28)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=22)    # legend fontsize

# plt.ticklabel_format(style='plain')
# plt.ylim(0, 0.8)

plt.xticks(msg_cnt)
plt.xlabel("Number of Aggregate Messages")
plt.bar(msg_cnt, ver_time, color='y', width=wid, label='Aggregate message verification')
# plt.plot(msg_cnt, sign_time, 'bo')

plt.ylabel("Time (seconds)")
# plt.plot(msg_cnt, ver_time, 'ro')

plt.legend()
plt.show()
