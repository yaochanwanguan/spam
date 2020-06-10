try {
  if (process.env.PORT_PUBLISHER) {
    publishDebugPort()
    return;
  }

  if (hasInspectArg()) {
    return;
  }

  if (isElectronRendererProcess()) {
    return;
  }

  try {
    if (!require('worker_threads').isMainThread) {
      // will be attached using WIP NodeWorker domain
      return;
    }
  }
  catch (ignored) {
  }
  let asyncInspectorOpenSupported = isAsyncInspectorOpenSupported();

  let inspector = require("inspector");
  const {execFile, execFileSync} = require('child_process');
  let port = findAvailablePort(inspector);
  let launchPortPublisher = asyncInspectorOpenSupported ? execFileSync : execFile;
  const interpreter = process.env["JB_INTERPRETER"] || process.execPath;
  launchPortPublisher(interpreter, [__filename], {
    env: {
      PORT_PUBLISHER: true,
      JB_PUBLISH_PORT: process.env["JB_PUBLISH_PORT"],
      JB_DEBUG_PORT: port
    },
    stdio: 'inherit'
  });
  if (!asyncInspectorOpenSupported) {
    inspector.open(port, undefined, true);
  }

}
catch (e) {
  console.error("Error in JetBrains node debug connector: ", e)
}

function publishDebugPort() {
  let publishPort = process.env["JB_PUBLISH_PORT"];
  let debugPort = process.env["JB_DEBUG_PORT"];

  const net = require('net');
  const TIMEOUT = 15000;
  const socket = net.createConnection(publishPort, () => {
    socket.on('data', (d) => {
      clearTimeout(timeoutId);
      socket.destroy();
    });

    socket.write(debugPort, "utf8");
    const timeoutId = setTimeout(() => {
      process.stderr.write("Debugger didn't connect during timeout\n")
      return socket.destroy();
    }, TIMEOUT);
  });
  socket.setNoDelay(true);
  socket.on('error', err => {
    process.stderr.write("Error in debuggerConnector: " + err.message + "\n" + err.stack);
    process.exit(0);
  });
}

function hasInspectArg() {
  return process.execArgv.find(
      arg => arg === "--inspect" || arg === "--inspect-brk" || arg.startsWith("--inspect-brk=") || arg.startsWith("--inspect=")
  );
}

function isElectronRendererProcess() {
  return process.type && process.type === "renderer" ||
         process.argv.indexOf("--type=renderer") >= 0;
}

/**
 * inspector.open(...,...,false) doesn't work properly on some node versions. It opens the port but debugger can't attach.
 */
function isAsyncInspectorOpenSupported() {
  try {
    let versions = process.versions.node.split(".");
    let major = parseInt(versions[0]);
    let minor = parseInt(versions[1]);
    let asyncInspectorOpenSupported = major >= 11 || (major === 10 && minor >= 7);
    return asyncInspectorOpenSupported;
  }
  catch (e) {
    process.stderr.write("Cannot parse node version: " + process.versions.node + "\n" + e.message);
    return false;
  }
}

function findAvailablePort(inspector) {
  try {
    let closeAuxiliaryInspector = !isAsyncInspectorOpenSupported();
    if (closeAuxiliaryInspector) {
      process.stderr.write("[IntelliJ is searching for port] ")
    }

    inspector.open(0, undefined, false);
    let url = inspector.url();
    let schemeSeparatorIndex = url.indexOf("://");
    let slashIndex = url.indexOf("/", schemeSeparatorIndex + 3);
    let colonIndex = url.substr(0, slashIndex).lastIndexOf(":");
    let portString = url.substr(colonIndex + 1, slashIndex - colonIndex - 1);
    let port = Number(portString);
    if (!port) throw Error("failed to parse " + url);

    if (closeAuxiliaryInspector) {
      inspector.close()
    }

    return port;
  }
  catch(e) {
    inspector.close();
    throw e;
  }
}