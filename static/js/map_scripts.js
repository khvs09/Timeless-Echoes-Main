document.addEventListener('DOMContentLoaded', function() {
    // Initialize map on article view page
    initArticleMap();
    
    // Initialize map on create/edit article page
    initCreateEditMap();
});

function initArticleMap() {
    // Check if we're on an article detail page with a map
    const mapContainer = document.getElementById('article-map');
    if (!mapContainer) return;
    
    // Get coordinates and data from data attributes
    const latitude = parseFloat(mapContainer.dataset.latitude);
    const longitude = parseFloat(mapContainer.dataset.longitude);
    const title = mapContainer.dataset.title;
    const location = mapContainer.dataset.location;
    
    if (isNaN(latitude) || isNaN(longitude)) return;
    
    // Initialize the map
    const map = L.map('article-map').setView([latitude, longitude], 12);
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add marker at the specified location
    const marker = L.marker([latitude, longitude]).addTo(map);
    
    // Create popup content
    const popupContent = `
        <div class="map-popup">
            <h4>${title}</h4>
            <p><i class="fas fa-map-marker-alt"></i> ${location}</p>
        </div>
    `;
    
    marker.bindPopup(popupContent).openPopup();
    
    // Add zoom control
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);
}

function initCreateEditMap() {
    // Check if we're on create/edit article page
    const mapContainer = document.getElementById('map-container');
    if (!mapContainer) return;
    
    // Get form fields
    const latField = document.getElementById('latitude');
    const lngField = document.getElementById('longitude');
    const searchInput = document.getElementById('location-search');
    
    // Default to center of India or use existing coordinates
    let initialLat = 20.5937;
    let initialLng = 78.9629;
    let initialZoom = 5;
    
    // If editing an article, use existing coordinates
    if (latField && latField.value && lngField && lngField.value) {
        initialLat = parseFloat(latField.value);
        initialLng = parseFloat(lngField.value);
        initialZoom = 12;
    }
    
    // Initialize the map
    const map = L.map('map-container', {
        center: [initialLat, initialLng],
        zoom: initialZoom,
        zoomControl: false // We'll add it manually
    });
    
    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Add zoom control to bottom right
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);
    
    // Add a marker if coordinates exist
    let marker;
    if (latField && latField.value && lngField && lngField.value) {
        marker = L.marker([initialLat, initialLng]).addTo(map);
    }
    
    // Add clear location button
    const clearButton = document.querySelector('.clear-location-btn');
    if (clearButton) {
        clearButton.style.display = marker ? 'block' : 'none';
    }
    
    // Add loading indicator
    const loadingDiv = document.querySelector('.search-loading');
    
    // Add map status div
    const mapStatus = document.querySelector('.map-status');
    
    // Handle clear location button click
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            if (marker) {
                map.removeLayer(marker);
                marker = null;
            }
            if (latField) latField.value = '';
            if (lngField) lngField.value = '';
            updateLocationFields({});
            updateMapStatus('Location cleared');
            this.style.display = 'none';
        });
    }
    
    // Handle map click to set marker
    map.on('click', function(e) {
        // Update the form fields
        if (latField && lngField) {
            latField.value = e.latlng.lat;
            lngField.value = e.latlng.lng;
            
            // Trigger a change event on the fields
            latField.dispatchEvent(new Event('change'));
            lngField.dispatchEvent(new Event('change'));
            
            // Perform reverse geocoding
            reverseGeocode(e.latlng.lat, e.latlng.lng);
        }
        
        // Update or add the marker
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker(e.latlng).addTo(map);
        }
        
        // Show clear button
        if (clearButton) {
            clearButton.style.display = 'block';
        }
        
        updateMapStatus('Location selected');
    });
    
    // Handle location search
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            // Clear previous timeout
            if (searchTimeout) {
                clearTimeout(searchTimeout);
            }
            
            // Show loading indicator
            if (loadingDiv) {
                loadingDiv.style.display = 'block';
            }
            
            // Set new timeout
            searchTimeout = setTimeout(() => {
                const searchQuery = this.value.trim();
                if (searchQuery.length < 3) {
                    if (loadingDiv) {
                        loadingDiv.style.display = 'none';
                    }
                    return;
                }
                
                // Use Nominatim for geocoding
                fetch(`/geocode?location=${encodeURIComponent(searchQuery)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.lat && data.lon) {
                            const lat = parseFloat(data.lat);
                            const lng = parseFloat(data.lon);
                            
                            // Update map view
                            map.setView([lat, lng], 12);
                            
                            // Update marker
                            if (marker) {
                                marker.setLatLng([lat, lng]);
                            } else {
                                marker = L.marker([lat, lng]).addTo(map);
                            }
                            
                            // Show clear button
                            if (clearButton) {
                                clearButton.style.display = 'block';
                            }
                            
                            // Update form fields
                            if (latField && lngField) {
                                latField.value = lat;
                                lngField.value = lng;
                                
                                // Trigger a change event on the fields
                                latField.dispatchEvent(new Event('change'));
                                lngField.dispatchEvent(new Event('change'));
                            }
                            
                            // Log the address data for debugging
                            console.log('Geocoding response:', data);
                            
                            // Update location fields
                            if (data.address) {
                                updateLocationFields(data.address);
                            }
                            
                            updateMapStatus('Location found');
                        }
                    })
                    .catch(error => {
                        console.error('Error searching for location:', error);
                        updateMapStatus('Error searching for location', true);
                    })
                    .finally(() => {
                        if (loadingDiv) {
                            loadingDiv.style.display = 'none';
                        }
                    });
            }, 500); // Debounce search for 500ms
        });
    }
    
    // Trigger a resize event after a short delay to ensure proper rendering
    setTimeout(() => {
        map.invalidateSize();
    }, 100);
}

function updateLocationFields(address) {
    if (!address) return;
    
    const stateField = document.getElementById('state');
    const districtField = document.getElementById('district');
    const villageField = document.getElementById('village');
    const addressField = document.getElementById('address');
    
    // Handle state field
    if (stateField) {
        if (address.state) {
            stateField.value = address.state;
        } else if (address.state_district) {
            stateField.value = address.state_district;
        }
    }
    
    // Handle district field
    if (districtField) {
        if (address.county) {
            districtField.value = address.county;
        } else if (address.district) {
            districtField.value = address.district;
        } else if (address.state_district) {
            districtField.value = address.state_district;
        }
    }
    
    // Handle village field
    if (villageField) {
        if (address.village) {
            villageField.value = address.village;
        } else if (address.town) {
            villageField.value = address.town;
        } else if (address.city) {
            villageField.value = address.city;
        } else if (address.suburb) {
            villageField.value = address.suburb;
        } else if (address.hamlet) {
            villageField.value = address.hamlet;
        }
    }
    
    // Handle address field
    if (addressField) {
        let addressParts = [];
        
        // Add village/town/city
        if (address.village) addressParts.push(address.village);
        else if (address.town) addressParts.push(address.town);
        else if (address.city) addressParts.push(address.city);
        else if (address.suburb) addressParts.push(address.suburb);
        else if (address.hamlet) addressParts.push(address.hamlet);
        
        // Add district/county
        if (address.county) addressParts.push(address.county);
        else if (address.district) addressParts.push(address.district);
        else if (address.state_district) addressParts.push(address.state_district);
        
        // Add state
        if (address.state) addressParts.push(address.state);
        
        // Add postcode if available
        if (address.postcode) addressParts.push(address.postcode);
        
        // Join all parts with commas and remove any empty strings
        addressField.value = addressParts.filter(part => part).join(', ');
    }
}

function reverseGeocode(lat, lng) {
    // Show loading state
    updateMapStatus('Loading location details...');
    
    fetch(`/api/reverse_geocode?lat=${lat}&lon=${lng}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.address) {
                // Log the address data for debugging
                console.log('Reverse geocoding response:', data.address);
                
                updateLocationFields(data.address);
                updateMapStatus('Location details loaded');
            } else {
                updateMapStatus('No location details found', true);
            }
        })
        .catch(error => {
            console.error('Error performing reverse geocoding:', error);
            updateMapStatus('Error loading location details', true);
        });
}

function updateMapStatus(message, isError = false) {
    const mapStatus = document.querySelector('.map-status');
    if (mapStatus) {
        mapStatus.innerHTML = `<p class="${isError ? 'error' : ''}">${message}</p>`;
        
        // Clear status after 3 seconds
        setTimeout(() => {
            mapStatus.innerHTML = '';
        }, 3000);
    }
} 