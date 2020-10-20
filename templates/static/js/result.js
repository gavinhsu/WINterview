$(function () {
    $('#container').highcharts({
        chart: {
            renderTo: 'container',
            plotBackgroundColor: null,
            plotBackgroundImage: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: 'Browser<br>shares<br>2015',
            align: 'center',
            verticalAlign: 'top',
            y: 40
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        pane: {
            center: ['50%', '75%'],
            size: '50%',
            startAngle: -90,
            endAngle: 90,
            background: {
            	borderWidth: 0,
                backgroundColor: 'none',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
		yAxis: [{
            lineWidth: 0,
	        min: 0,
	        max: 90,
            minorTickLength: 0,
            tickLength: 0,
            tickWidth: 0,
	        labels: {
	        	enabled: false
	        },
            title: {
                text: '', //'<div class="gaugeFooter">46% Rate</div>',
                useHTML: true,
                y: 80
            },
	        /*plotBands: [{
	        	from: 0,
	        	to: 46,
	        	color: 'pink',
	        	innerRadius: '100%',
	        	outerRadius: '0%'
	        },{
	        	from: 46,
	        	to: 90,
	        	color: 'tan',
	        	innerRadius: '100%',
	        	outerRadius: '0%'
	        }],*/
	        pane: 0,
	        
	    }],
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%']
            },
            gauge: {
	    		dataLabels: {
	    			enabled: false
	    		},
	    		dial: {
	    			radius: '100%'
	    		}
	    	}
        },
     
        series: [{
            type: 'pie',
            name: 'Browser share',
            innerSize: '50%',
            data: [
                ['POOR',   25],
                ['FAIR',       25],
                ['GOOD', 25],
                ['EXCELLENT',     25]
            ]
        },{
            type: 'gauge',
            data: [40],
            dial: {
                rearLength: 0
            }
        }],
    });    
});

