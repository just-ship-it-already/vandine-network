// Add these variables at the beginning of the script section
let singleTestResult = null;
let multiTestResult = null;

// Add this new function to display cached results
function displayTestResults() {
    const results = document.getElementById("perfResults");
    let html = "";
    
    if (singleTestResult && multiTestResult) {
        // Show side-by-side comparison
        const speedup = (multiTestResult.throughput / singleTestResult.throughput).toFixed(1);
        const efficiencyPct = ((speedup / 4) * 100).toFixed(0);
        
        html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;">' +
            '<div style="background:rgba(0,0,0,0.3);padding:1rem;border-radius:0.5rem;border:1px solid rgba(255,158,11,0.3);">' +
            '<h4 style="color:var(--warning);margin-bottom:0.5rem;font-size:1rem;">🔸 Single Thread</h4>' +
            '<div style="font-size:0.9rem;">' +
            '• Processing Time: <span style="color:var(--warning);font-weight:600;">' + singleTestResult.time + 'ms</span><br>' +
            '• Operations: ' + singleTestResult.ops.toLocaleString() + '<br>' +
            '• Throughput: <span style="color:var(--warning);">' + singleTestResult.throughput + '</span> ops/ms<br>' +
            '• CPU Usage: ' + singleTestResult.cpu + '%' +
            '</div></div>' +
            '<div style="background:rgba(0,0,0,0.3);padding:1rem;border-radius:0.5rem;border:1px solid rgba(0,255,136,0.3);">' +
            '<h4 style="color:var(--cyber);margin-bottom:0.5rem;font-size:1rem;">🔹 Multi Thread (4 cores)</h4>' +
            '<div style="font-size:0.9rem;">' +
            '• Processing Time: <span style="color:var(--cyber);font-weight:600;">' + multiTestResult.time + 'ms</span><br>' +
            '• Operations: ' + multiTestResult.ops.toLocaleString() + '<br>' +
            '• Throughput: <span style="color:var(--cyber);">' + multiTestResult.throughput + '</span> ops/ms<br>' +
            '• CPU Usage: ' + multiTestResult.cpu + '%' +
            '</div></div></div>' +
            '<div style="text-align:center;margin-top:1rem;padding:1rem;background:rgba(0,255,136,0.1);border-radius:0.5rem;border:1px solid rgba(0,255,136,0.2);">' +
            '<div style="font-size:1.2rem;">Multi-core Performance: <span style="color:var(--cyber);font-size:1.5rem;font-weight:700;">' + speedup + 'x</span> faster</div>' +
            '<div style="font-size:0.9rem;color:rgba(255,255,255,0.7);margin-top:0.5rem;">Parallel efficiency: ' + efficiencyPct + '% (' + speedup + 'x speedup on 4 cores)</div></div>';
    } else if (singleTestResult) {
        // Show only single test result
        html = '<div style="background:rgba(0,0,0,0.3);padding:1rem;border-radius:0.5rem;margin-top:1rem;border:1px solid rgba(255,158,11,0.3);">' +
            '<h4 style="color:var(--warning);margin-bottom:0.5rem;">🔸 Single Thread Results:</h4>' +
            '<div style="font-size:0.9rem;">' +
            '• Processing Time: ' + singleTestResult.time + 'ms<br>' +
            '• Operations: ' + singleTestResult.ops.toLocaleString() + '<br>' +
            '• Throughput: ' + singleTestResult.throughput + ' ops/ms<br>' +
            '• CPU Usage: ' + singleTestResult.cpu + '%' +
            '</div>' +
            '<div style="margin-top:0.5rem;font-size:0.85rem;color:rgba(255,255,255,0.6);">' +
            '⏳ Run the multi-thread test to see performance comparison...</div></div>';
    } else if (multiTestResult) {
        // Show only multi test result
        html = '<div style="background:rgba(0,0,0,0.3);padding:1rem;border-radius:0.5rem;margin-top:1rem;border:1px solid rgba(0,255,136,0.3);">' +
            '<h4 style="color:var(--cyber);margin-bottom:0.5rem;">🔹 Multi Thread Results:</h4>' +
            '<div style="font-size:0.9rem;">' +
            '• Processing Time: ' + multiTestResult.time + 'ms<br>' +
            '• Operations: ' + multiTestResult.ops.toLocaleString() + '<br>' +
            '• Throughput: ' + multiTestResult.throughput + ' ops/ms<br>' +
            '• CPU Usage: ' + multiTestResult.cpu + '%' +
            '</div>' +
            '<div style="margin-top:0.5rem;font-size:0.85rem;color:rgba(255,255,255,0.6);">' +
            '⏳ Run the single-thread test to see performance comparison...</div></div>';
    }
    
    results.innerHTML = html;
}
