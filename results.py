import matplotlib.pyplot as plt
import numpy as np

msg_size = [128,     256,     1024,     4096,    8192,
            32768,   65536, ]

sign_time = [0.1617,
             0.1639,
             0.1714,
             0.1966,
             0.2448,
             0.4222,
             0.7262,
             ]

ver_time = [0.0621,
            0.0657,
            0.0633,
            0.0683,
            0.0711,
            0.1048,
            0.1388,
            ]

# msg_cnt = [4, 10, 25, 50, 100]
# sign_time = [0.0694, 0.1315, 0.3014, 0.6194, 1.1913]
# ver_time = [0.0787, 0.1450, 0.3172, 0.6212, 1.200]

# fig, axs = plt.subplots((10, 10))
plt.figure(figsize=(9, 7))
plt.rc('font', size=16)          # controls default text sizes
plt.rc('axes', labelsize=28)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=22)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize

plt.ticklabel_format(style='plain')
plt.ylim(0, 0.8)

plt.xscale('log')
plt.xlabel("Size of Message (bytes)")
plt.plot(msg_size, sign_time, 'b', label='Single message signing')
plt.plot(msg_size, sign_time, 'bo')

plt.xticks(msg_size)
plt.xscale('log')
# axs.set_xscale('log')
# axs.set_xticks(msg_size)
# axs.get_xaxis().get_major_formatter().labelOnlyBase = False

# plt.yscale('log')
plt.ylabel("Time (seconds)")

plt.legend()
plt.show()

###############################################3

# fig, axs = plt.subplots((10, 10))
plt.figure(figsize=(9, 7))
plt.rc('font', size=16)          # controls default text sizes
plt.rc('axes', labelsize=28)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
plt.rc('legend', fontsize=18)    # legend fontsize

plt.ticklabel_format(style='plain')
plt.ylim(0, 0.20)
plt.yticks(np.arange(0, 0.21, 0.05))

# plt.xscale('log')
plt.xlabel("Size of Message (bytes)")
plt.plot(msg_size, ver_time, 'r', label='Single message verification')
plt.plot(msg_size, ver_time, 'ro')

plt.xticks(msg_size)
plt.xscale('log')
# axs.set_xscale('log')
# axs.set_xticks(msg_size)
# axs.get_xaxis().get_major_formatter().labelOnlyBase = False

# plt.yscale('log')
plt.ylabel("Time (seconds)")

plt.legend()
plt.show()
