from matplotlib import pyplot as plt
import turtle as t


def plot_PCN(airport_name, infomation):
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_alpha(0.)
    ax.axis('off')
    # 中文

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('标高和跑道长度为米，方位为磁方位\nRWY: PCN {}'.format(infomation), fontdict={'fontsize': 35})

    path = '../pythonProject/airport_data/{}/机坪PCN值.png'.format(airport_name)
    plt.savefig(path, format='png')
    plt.close()


if __name__ == '__main__':
    plot_PCN(123, 123)
