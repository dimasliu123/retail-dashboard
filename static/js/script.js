// Change Scale 
export const changeScale = (x) => { 
    return null;
}
export const getData = (total, member, non_member) => {
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

export const getConfig = (data) => {
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
                    font : {weight : "bold", size : 24}
                }
            },
            scales : {
                x : [{
                    type : "timeseries",
                }]
            }
        }
    }
    return config;
}
