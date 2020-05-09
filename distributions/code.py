import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
n = 2000
x1 = np.random.normal(0, 1, n)
x2 = np.random.gamma(2, 1.5, n)
x3 = np.random.exponential(2, n)
x4 = np.random.uniform(-2.5, 2.5, n)

def update_plot(curr):
    index = 100 + curr*50
    if index >= n: 
        a.event_source.stop()
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    
    # plot the histograms
    ax1.hist(x1[:index], density=True, bins=75, alpha=0.8)
    ax2.hist(x2[:index], density=True, bins=75, alpha=0.8)
    ax3.hist(x3[:index], density=True, bins=75, alpha=0.8)
    ax4.hist(x4[:index], density=True, bins=75, alpha=0.8)

    # set axes, labels, and text
    ax1.set_xlim([-5, 10])
    ax1.set_ylim([0, 0.5])
    ax1.set_yticks([])
    ax1.set_title('Sampling Various Distribution, Sample Size = ' + str(index))
    ax1.text(7.0, 0.25, 'Normal')
    ax2.text(7.0, 0.25, 'Gamma')
    ax3.text(7.0, 0.25, 'Exponential')
    ax4.text(7.0, 0.25, 'Uniform')
    

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, sharey=True)
a = animation.FuncAnimation(fig, update_plot, interval=5)
plt.show()
