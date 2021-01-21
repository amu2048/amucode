import * as echarts from '../lib/ec-canvas/echarts';
const app = getApp();

Page({
  /**
   * 页面的初始数据
   */
  data: {
    line_ec: {
      lazyLoad: true // 延迟加载
    }, //折线图
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function() {
    this.linechartsComponnet = this.selectComponent('#businessTrend'); //折线图
  },

  //初始化图表--折线图
  init_lineCharts: function() {
    this.linechartsComponnet.init((canvas, width, height) => {
      // 初始化图表
      const lineChart = echarts.init(canvas, null, {
        width: width,
        height: height
      });

      lineChart.setOption(this.getLineOption());

      //此处为折线图的点击事件，点击展示折点信息
      lineChart.on('click', function(handler, context) {
        var handlerValue = handler.name + ' :  ' + handler.value
        wx.showToast({
          title: handlerValue,
          icon: 'none',
          duration: 1200,
          mask: true
        })
      });
      return lineChart;
    });
  },

  /**
   * 折线图
   */
  getLineOption: function() {
    var option = {
      title: {
        text: '营业趋势'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
        },
      },
      toolbox: {
        show: true,
        feature: {
          mark: {
            show: true
          },
          dataView: {
            show: true,
            readOnly: false
          },
          restore: {
            show: true
          },
          saveAsImage: {
            show: true
          }
        }
      },
      legend: {
        data: ['营业趋势']
      },
      grid: {
        left: '3%',
        bottom: '3%',
        containLabel: true
      },
      toolbox: {
        show: true,
        feature: {
          mark: {
            show: true
          },
          dataView: {
            show: true,
            readOnly: false
          },
          magicType: {
            show: true,
            type: ['line', 'bar', 'stack', 'tiled']
          },
          restore: {
            show: true
          },
          saveAsImage: {
            show: true
          }
        }
      },
      calculable: true,
      xAxis: [{
        type: 'category',
        boundaryGap: false,
        data: this.data.consumeDay,//此处为数组
        axisLabel: {
          interval: this.data.interval, //x轴间隔多少显示刻度
          fontSize: 8,
        }
      }],
      yAxis: [{
        type: 'value',
        axisLine: {
          show: true
        },
        axisTick: {
          show: true
        },
      }],
      series: [{
        name: '营业趋势',
        type: 'line',
        smooth: true,
        center: ['100%', '100%'],
        itemStyle: {
          normal: {
            color: '#56cbff',
            fontSize: '80',
            lineStyle: {
              color: '#56cbff'
            },
            areaStyle: {
              color: 'rgb(230,249,252)'
            },
          }
        },
        data: this.data.consumeAmount,//此处为数组
      }]
    };
    return option;
  },
});
