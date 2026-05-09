// Global script to handle potential DOM issues and prevent common errors

// Function to safely add event listeners to elements that may not exist yet
function safeAddEventListener(selector, event, handler, options = {}) {
  // Check if element exists first
  const element = document.querySelector(selector);
  if (element) {
    element.addEventListener(event, handler, options);
    return true;
  }
  
  // If element doesn't exist yet, wait for DOM to be ready and try again
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      const element = document.querySelector(selector);
      if (element) {
        element.addEventListener(event, handler, options);
      }
    });
    return true;
  }
  
  // If DOM is already loaded, try to find the element later
  const observer = new MutationObserver(() => {
    const element = document.querySelector(selector);
    if (element) {
      element.addEventListener(event, handler, options);
      observer.disconnect(); // Stop observing once we find the element
    }
  });
  
  // Start observing for changes to the DOM
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  return false; // Element not found yet, but will try when it appears
}

// Global error handler to catch and log errors more gracefully
window.addEventListener('error', (event) => {
  console.error('Global error caught:', event.error);
  
  // Specifically handle the addEventListener error
  if (event.error && event.error.message && 
      event.error.message.includes('Cannot read properties of null')) {
    console.warn('Potential null reference error caught:', event.error);
  }
});

// Make safeAddEventListener available globally if needed
window.safeAddEventListener = safeAddEventListener;

// Safe function to handle potential share modal issues
document.addEventListener('DOMContentLoaded', function() {
  // Check if there's a share modal element that might be causing issues
  const shareModalElements = document.querySelectorAll('[id*="share"], [class*="share"], [data-modal*="share"]');
  
  shareModalElements.forEach(element => {
    // Add event listeners safely with error handling
    try {
      if (element) {
        // Example: safely add click handlers
        element.addEventListener('click', function(e) {
          console.log('Share element clicked:', element);
        });
      }
    } catch (error) {
      console.warn('Could not add event listener to share element:', error);
    }
  });
});