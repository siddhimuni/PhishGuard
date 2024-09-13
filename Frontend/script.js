document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        let activeTab = tabs[0];
        let activeTabUrl = activeTab.url;

        // Capture the screenshot
        chrome.tabs.captureVisibleTab(activeTab.windowId, { format: 'png' }, function(dataUrl) {
            // Create an image element to display the screenshot
            // let img = document.createElement('img');
            // img.src = dataUrl;
            // img.alt = 'Screenshot';
            // img.style.maxWidth = '100%'; // Adjust as needed
            // document.getElementById('screenshot').appendChild(img);

            fetch('http://127.0.0.1:5000/screenshotDetection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: dataUrl })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                document.getElementById('ss').innerText = `Website is ${data}`;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });


        // Display the URL
        fetch('http://127.0.0.1:5000/htmlPhished', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                'url': activeTabUrl 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('html').innerText = `Website is ${JSON.stringify(data, null, 2)} % safe`;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

        //
        fetch('http://127.0.0.1:5000/urlDetection', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({
                'url': activeTabUrl 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('url').innerText = `Website is ${data}`;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });
});
