// Viewport Testing Tool
document.addEventListener('DOMContentLoaded', function() {
    // Create testing toolbar
    const toolbar = document.createElement('div');
    toolbar.id = 'testing-toolbar';
    toolbar.style.cssText = `
        position: fixed;
        top: 0;
        right: 0;
        background: #2563eb;
        color: white;
        padding: 10px;
        border-bottom-left-radius: 5px;
        z-index: 10000;
        font-family: -apple-system, system-ui, sans-serif;
        display: flex;
        gap: 10px;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    `;

    // Create viewport info display
    const viewportDisplay = document.createElement('div');
    viewportDisplay.id = 'viewport-info';
    viewportDisplay.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 9999;
        font-family: monospace;
        pointer-events: none;
        transition: opacity 0.3s;
    `;
    document.body.appendChild(viewportDisplay); Tool
document.addEventListener('DOMContentLoaded', function () {
  // Create viewport info display
  const viewportDisplay = document.createElement('div');
  viewportDisplay.id = 'viewport-info';
  viewportDisplay.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 9999;
        font-family: monospace;
        pointer-events: none;
    `;
  document.body.appendChild(viewportDisplay);

  // Create device selector
  const deviceSelector = document.createElement('div');
  deviceSelector.id = 'device-selector';
  deviceSelector.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 9999;
    `;

  const devices = {
    Desktop: '1920x1080',
    Laptop: '1366x768',
    Tablet: '768x1024',
    'Mobile L': '425x850',
    'Mobile M': '375x667',
    'Mobile S': '320x568',
  };

  deviceSelector.innerHTML = `
        <select id="device-select" style="padding: 5px; margin-right: 10px;">
            ${Object.keys(devices)
              .map(
                (device) =>
                  `<option value="${devices[device]}">${device} (${devices[device]})</option>`
              )
              .join('')}
        </select>
        <button id="toggle-debug" style="padding: 5px 10px;">Toggle Debug</button>
    `;
  document.body.appendChild(deviceSelector);

  // Update viewport info
  function updateViewportInfo() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const breakpoint =
      width <= 480 ? 'mobile' : width <= 768 ? 'tablet' : 'desktop';

    viewportDisplay.innerHTML = `
            Width: ${width}px<br>
            Height: ${height}px<br>
            Breakpoint: ${breakpoint}<br>
            Device Pixel Ratio: ${window.devicePixelRatio}
        `;
  }

  // Add debug outline
  function toggleDebugMode() {
    const debugStyle = document.getElementById('debug-style');
    if (debugStyle) {
      debugStyle.remove();
    } else {
      const style = document.createElement('style');
      style.id = 'debug-style';
      style.innerHTML = `
                * {
                    outline: 1px solid rgba(255, 0, 0, 0.2) !important;
                }
                * * {
                    outline: 1px solid rgba(0, 255, 0, 0.2) !important;
                }
                * * * {
                    outline: 1px solid rgba(0, 0, 255, 0.2) !important;
                }
            `;
      document.head.appendChild(style);
    }
  }

  // Event listeners
  window.addEventListener('resize', updateViewportInfo);
  document.getElementById('device-select').addEventListener('change', (e) => {
    const [width, height] = e.target.value.split('x');
    window.resizeTo(parseInt(width), parseInt(height));
  });
  document
    .getElementById('toggle-debug')
    .addEventListener('click', toggleDebugMode);

  // Initial update
  updateViewportInfo();
});
