/** Fetch weather data for the selected location */
function fetchWeatherData()
{
    const weather = document.querySelector('span[data-weather]');
    const locationId = parseInt(this.value);
    const locationOptionName = this.options[this.selectedIndex].text;
    const wrapper = document.querySelector('[data-weather-wrapper]');

    if (isNaN(locationId)) {
        weather.textContent = 'Select a location to get weather data.';
        wrapper.style.backgroundColor = '';
        return;
    }

    const fetchInit = window.fetchConfig();
    fetchInit.body = JSON.stringify({
        location_id: locationId,
        task_id: window.location.pathname.split('/')[2] || null,
    });

    fetch(`/task/weather/`, fetchInit)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(function(message) {
            const data = JSON.parse(message);
            if (data.error) {
                weather.textContent = 'Cannot load weather data. Please try again later.';
                return;
            }

            // Set weather plugin element text
            weather.textContent = `${data.description.title}, ${data.description.condition.name} in ${locationOptionName}`;
            wrapper.style.backgroundColor = data.description.condition.color;

            // Add weather data to form input
            document.querySelector('input[name="weather"]').value = JSON.stringify(data);
        }).catch(function() {
        weather.textContent = 'Cannot load weather data. Please try again later.';
    })
}

document.addEventListener('DOMContentLoaded', function() {
    const locationList = document.querySelector('select#id_location');
    const refreshButton = document.querySelector('input[data-refresh]')
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            locationList.dispatchEvent(new Event('change'));
        });
    }
    locationList.addEventListener('change', function() {
        fetchWeatherData.call(this);
    });
});
