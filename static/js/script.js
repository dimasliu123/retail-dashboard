export const getSalesData = (total, member, non_member) => {
    const data = { 
        datasets : [
            {
                label : "Total Sales",
                data : total,
                fill : false,
                borderColor : "#0080FF",
                backgroundColor : "transparent",
                tension : 0.15,
            },
            {
                label : "Member Sales",
                data : member,
                fill : false,
                borderColor : "#DC143C",
                backgroundColor : "transparent",
                tension : 0.15,
            },
            {
                label : "Non Member Sales",
                data : non_member,
                fill : false,
                borderColor : "#50C878",
                backgroundColor : "transparent",
                tension : 0.15,
            }
        ]
    }
    return data;
}

export const getSalesConfig = (data) => {
    const config = {
        type : "line",
        data : data,
        options : {
            responsive : true,
            interaction : {
                mode : "index",
                intersect : false,
            },
            plugins : {
                title : {
                    display : true,
                    text : "Daily Sales",
                    font : {weight : "bold", size : 24, family : "optima"}
                }
            },
            scales : {
                x : [{
                    type : "time",
                    distributed : "series",
                }]
            }
        }
    }
    return config;
}


export const getRFMScore = (Label, Value) => {
    const data = {
        labels : Label,
        datasets : [{
            data : Value,
            backgroundColor : [
                "#FF638433",
                "#FF9F4033",
                "#FFCD5633",
                "#4BC0C033",
                "#36A2EB33",
                "#9966FF33",
                "#C9CBCF33",
                "#FFE6FF33",
                "#CCFFE633",
            ],
            borderColor : [
                "#FF6384",
                "#FF9F40",
                "#FFCD56",
                "#4BC0C0",
                "#36A2EB",
                "#9966FF",
                "#C9CBCF",
                "#FF99FF",
                "#4DFFA6",
            ],
            borderWidth : 1,
        }]
    }
    return data
}

export const RFMScoreConfig = (Data) => {
    const rfm_data = {
        type : "bar",
        data : Data,
        options : {
            responsive : true,
            plugins : {
                title : {
                    display : true,
                    text : "RFM Score",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                },
            },
            scale : {
                y : {
                    beginAtZero :false 
                },
            },
        }
    }
    return rfm_data
};

const randomColorGenerator = (numColor) => { 
    const arrColor = [];
    const arrBorderColor = [];
    for (let i = 0; i < numColor; i++) {
        let randColor =  '#' + (Math.random().toString(16) + '0000000').slice(2, 8)
        arrColor.push(randColor + "33")
        arrBorderColor.push(randColor)
    }
    return {bgColor : arrColor, borderColor : arrBorderColor} 
};

export const rfmClassData = (labels, total) => {
    const color = randomColorGenerator(6)
    const data = { 
        labels : labels,
        datasets: [{
            data: total,
            backgroundColor : color.bgColor,
            borderColor : color.borderColor,
        }]
    }
    return data;
}

export const rfmClassConfig = (data) => {
    const config = {
        type : "bar",
        data : data,
        options : {
            responsive : true,
            plugins : {
                title : {
                    display : true,
                    text : "RFM Class",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                },
                scale : {
                    y : {
                        beginAtZero : false,
                    },
                    xAxes : [{
                        barThickness : 6,
                        maxBarThickness : 6,
                    }],
                },
            }
        }
    }
    return config;
}

export const findArr = (date_arr, country_arr, sales_arr, cond) => {
    const foundCountry = [];
    const foundSales = [];
    for (let i=0; i < date_arr.length; i++) {
        if (date_arr[i] == cond) {
            foundCountry.push(country_arr[i]);
            foundSales.push(sales_arr[i]);
        }
    }
    return {Country : foundCountry, Sales : foundSales };
}

export const countryData = (labels, total) => {
    const color = randomColorGenerator(6)
    const data = { 
        labels : labels,
        datasets: [{
            data: total,
            backgroundColor : color.bgColor,
            borderColor : color.borderColor,
        }]
    }
    return data;
}

export const countryConfig = (data) => {
    const config = {
        type : "bar",
        data : data,
        options : {
            responsive : true,
            plugins : {
                title : {
                    display : true,
                    text : "Monthly Sales (Country)",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                },
                scale : {
                    y : {
                        beginAtZero : false,
                    },
                    xAxes : [{
                        barThickness : 6,
                        maxBarThickness : 6,
                    }],
                },
            }
        }
    }
    return config;
}

