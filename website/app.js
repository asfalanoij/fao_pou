document.addEventListener('DOMContentLoaded', function() {
    // Chart 1: Child Malnutrition
    fetch('malnutrition_data.json')
        .then(response => response.json())
        .then(data => {
            const stuntingData = data.filter(d => d.Item.includes('stunted'));
            const wastingData = data.filter(d => d.Item.includes('wasting'));

            const countries = [...new Set(data.map(d => d.Area))];

            const stuntingTraces = countries.map(country => {
                const countryData = stuntingData.filter(d => d.Area === country);
                return {
                    x: countryData.map(d => d.Year),
                    y: countryData.map(d => d.Value),
                    mode: 'lines+markers',
                    name: country
                };
            });

            const wastingTraces = countries.map(country => {
                const countryData = wastingData.filter(d => d.Area === country);
                return {
                    x: countryData.map(d => d.Year),
                    y: countryData.map(d => d.Value),
                    mode: 'lines+markers',
                    name: country,
                    xaxis: 'x2',
                    yaxis: 'y2',
                    showlegend: false
                };
            });

            const layout = {
                title: 'Child Malnutrition: Stunting vs. Wasting (%)',
                grid: {rows: 2, columns: 1, pattern: 'independent'},
                xaxis: { title: 'Year' },
                yaxis: { title: 'Stunting (%)' },
                xaxis2: { title: 'Year' },
                yaxis2: { title: 'Wasting (%)' },
                template: 'plotly_white',
                height: 700
            };

            Plotly.newPlot('malnutrition-chart', [...stuntingTraces, ...wastingTraces], layout);
        });

    // Chart 2: Gender Disparity
    fetch('gender_data.json')
        .then(response => response.json())
        .then(data => {
            const femaleData = data.filter(d => d.Item.includes('female'));
            const maleData = data.filter(d => d.Item.includes('male'));

            const trace1 = {
                x: femaleData.map(d => d.Area),
                y: femaleData.map(d => d.Value),
                name: 'Female',
                type: 'bar'
            };

            const trace2 = {
                x: maleData.map(d => d.Area),
                y: maleData.map(d => d.Value),
                name: 'Male',
                type: 'bar'
            };

            const layout = {
                title: 'Gender Disparity in Severe Food Insecurity (Latest Year)',
                barmode: 'group',
                xaxis: { title: 'Country' },
                yaxis: { title: 'Prevalence (%)' },
                template: 'plotly_white'
            };

            Plotly.newPlot('gender-chart', [trace1, trace2], layout);
        });

    // Chart 3: Anemia
    fetch('anemia_data.json')
        .then(response => response.json())
        .then(data => {
            const countries = [...new Set(data.map(d => d.Area))];

            const traces = countries.map(country => {
                const countryData = data.filter(d => d.Area === country);
                return {
                    x: countryData.map(d => d.Year),
                    y: countryData.map(d => d.Value),
                    mode: 'lines+markers',
                    name: country
                };
            });

            const layout = {
                title: 'Anemia Among Women of Reproductive Age (15-49 years)',
                xaxis: { title: 'Year' },
                yaxis: { title: 'Prevalence (%)' },
                template: 'plotly_white'
            };

            Plotly.newPlot('anemia-chart', traces, layout);
        });
});
