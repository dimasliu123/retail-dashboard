// Sales Page
export const getSalesData = (total, member, non_member) => {
    const data = { 
        datasets : [
            {
                label : "Total Sales",
                data : total,
                fill : false,
                borderColor : "#0080FF",
                backgroundColor : "transparent",
                tension : 0.20,
            },
            {
                label : "Member Sales",
                data : member,
                fill : false,
                borderColor : "#DC143C",
                backgroundColor : "transparent",
                tension : 0.20,
            },
            {
                label : "Non Member Sales",
                data : non_member,
                fill : false,
                borderColor : "#50C878",
                backgroundColor : "transparent",
                tension : 0.20,
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
                    color : "#F5F5F5",
                    font : {weight : "bold", size : 26, family : "optima"}
                },
                legend : {
                    labels : {
                        color : "#F5F5F5",
                    }
                }
            },
            scales : {
                x : {
                    ticks : {
                        color : "#F5F5F5",
                    },
                    grid : {
                    },
                },
                y: {
                    type : "linear",
                    ticks : {
                        color : "#F5F5F5",
                    },
                    grid : {
                    },
                },
            },
        }
    }
    return config;
}
// Sales Page

// Customer Page

export const getRFMScore = (Label, Value) => {
    const data = {
        labels : Label,
        datasets : [{
            data : Value,
            backgroundColor : [
                "#FF638433", "#FF9F4033", "#FFCD5633",
                "#4BC0C033", "#36A2EB33", "#9966FF33",
                "#C9CBCF33", "#FFE6FF33", "#CCFFE633",],
            borderColor : [
                "#FF6384", "#FF9F40", "#FFCD56",
                "#4BC0C0", "#36A2EB", "#9966FF",
                "#C9CBCF", "#FF99FF", "#4DFFA6",],
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
                    color : "#F5F5F5",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                },
            },
            scales : {
                x : {
                    ticks : {
                         color : "#F5F5F5",
                    },
                },
                y : {
                    beginAtZero : true,
                    ticks : {
                        color : "#F5F5F5",
                    },
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
        arrColor.push(randColor + "66")
        arrBorderColor.push(randColor)
    }
    return { bgColor : arrColor, borderColor : arrBorderColor } 
};

export const randColorGenerator = (numColor) => { 
    const arrColor = [];
    for (let i = 0; i < numColor; i++) {
        let randColor =  '#' + (Math.random().toString(16) + '0000000').slice(2, 8)
        arrColor.push(randColor)
    }
    return arrColor 
};


export const rfmClassData = (labels, total) => {
    const color = randomColorGenerator(labels.length)
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
                    color : "#F5F5F5",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                }, 
            }, scales : {
                xAxes : {
                    display : true,
                    ticks : { color : "#F5F5F5" },
                    barThickness : 10,
                    maxBarThickness :10,
                    scaleLabel : {
                        display : true,
                        fontColor : "#F5F5F5",
                    },
                },
                yAxes : {
                    display : true,
                    ticks : { color : "#F5F5F5" },
                    scaleLabel : {
                        display : true,
                        fontColor : "#F5F5F5",
                    }
                },
            },
        }
    }
    return config;
}

// Customer Page

// Country Page
export const getCountryData = (country, sales) => {
    let color = randomColorGenerator(country.length) ;
    const data = {
        labels : country,
        datasets : [
            {
                label : "Country Sales",
                backgroundColor : color.bgColor,
                borderColor : color.borderColor,
                data : sales
            }
        ]
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
                    color : "#F5F5F5",
                    font : {weight : "bold", size : 20, family : "optima"},
                },
                legend : {
                    display : false,
                    color : "#F5F5F5",
                },
            },
            scales : {
                y : {
                    type : "linear",
                    beginAtZero : false,
                    ticks : {
                        color : "#F5F5F5",
                        type : "linear",
                    },
                },
                x : {
                    ticks : {
                        color : "#F5F5F5",
                    },
                },
            },
        }
    }
    return config;
}

export function findSales (input_date, date_data, country_data, sales_data) {
    const num_array = date_data.length

    const selected_country = []
    const selected_sales = []

    for (let i = 0; i < num_array; i++) {
        if (date_data[i] == input_date) {
            let i_country = country_data[i]
            let i_sales = sales_data[i]
            selected_country.push(i_country)
            selected_sales.push(i_sales)
        }
    }
    return [selected_country, selected_sales]
}

export const getMaximumVal = (salesData) => {
    let max_sales = 0;
    for (let i = 0; i < salesData.length; i++) {
        max_sales += salesData[i]
    }
    return Math.round((max_sales + Number.EPSILON) * 100 ) / 100;
}

// Country Page