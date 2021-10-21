const router = require('express').Router();
const path = require('path');
const exec = require('child_process').exec;
const { PythonShell } = require('python-shell');

// setup a default "scriptPath"
PythonShell.defaultOptions = { scriptPath: path.join(__dirname, '../../../') };

function shutdown(callback) {
    exec('shutdown -r now', function(error, stdout, stderr) { callback(stdout); });
}

function killscript() {
    let pid;
    exec('pgrep -f btc_ticker.py', function(err, stdout, stderr) {
        console.log('stdout' + stdout);
        pid = stdout;
        console.log('pid ' + pid);
        if (pid) {
            exec('kill ' + pid, function(err, stdout, stderr) {
                console.log(stdout);
            });
        }
    });
}

//Main page
router.get('/', (req, res) => {
    res.render('index');
})

//Router to reboot
router.post("/reboot", (req, res) => {
    shutdown(function(output) {
        console.log(output);
    });
})

//Router to start in price mode
router.post("/start_price", (req, res) => {
    let { currency, refresh } = req.body;
    let options;
    const messages = [];

    try {
        killscript();
    } catch (e) {
        console.log('process not running');
    }
    if(currency === 'sats / USD') {
        currency = 'USD';
        options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ['-d', 'PRICE', '-t', refresh, '-c', currency, '-n', 'yes', '-s']
        };
    }
    else if(currency === 'sats / EUR') {
        currency = 'EUR';
        options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ['-d', 'PRICE', '-t', refresh, '-c', currency, '-n', 'yes', '-s']
        };
    }
    else {
        options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ['-d', 'PRICE', '-t', refresh, '-c', currency, '-n', 'yes']
        };
    }

    python_process = PythonShell.run('btc_ticker.py', options, function(err, result) {
        if (err) throw err;
    });
    messages.push({ text: "bitclock started in price mode!" });
    res.render("index", {
        messages
    });
});

//Router to start in block mode
router.post("/start_block", (req, res, next) => {
    const messages = [];
    const { currency, refresh } = req.body;
    try {
        killscript();
    } catch (e) {
        console.log('process not running');
    }

    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: ['-d', 'BLOCK', '-t', refresh, '-c', currency, '-n', 'yes']
    };

    python_process = PythonShell.run('btc_ticker.py', options, function(err, result) {
        if (err) throw err;
    });
    messages.push({ text: "bitclock started in block mode!" });
    res.render("index", {
        messages
    });
});

//Router to start in alternating mode
router.post("/start_multi", (req, res, next) => {
    const messages = [];
    const { currency, refresh } = req.body;
    try {
        killscript();
    } catch (e) {
        console.log('process not running');
    }

    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: ['-d', 'PRCBLK', '-t', refresh, '-c', currency, '-n', 'yes']
    };

    python_process = PythonShell.run('btc_ticker.py', options, function(err, result) {
        if (err) throw err;
    });

    messages.push({ text: "bitclock started in alternating mode!" });
    res.render("index", {
        messages
    });
});

//Router to start in quotes mode
router.post("/start_quotes", (req, res, next) => {
    const messages = [];
    const { currency, refresh } = req.body;
    try {
        killscript();
    } catch (e) {
        console.log('process not running');
    }

    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: ['-d', 'QUOTES', '-t', refresh, '-c', currency, '-n', 'yes']
    };

    python_process = PythonShell.run('btc_ticker.py', options, function(err, result) {
        if (err) throw err;
    });

    messages.push({ text: "bitclock started in QUOTE mode!" });
    res.render("index", {
        messages
    });
});

// this stops the process
router.post('/stop', function(req, res) {
    const messages = [];
    const { currency, refresh } = req.body;
    try {
        killscript();
    } catch (e) {
        console.log('process not running');
    }
    messages.push({ text: "bitclock stopped!" });
    res.render("index", {
        messages
    });
});

module.exports = router;