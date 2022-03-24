import java

lineSeparator = java.lang.System.getProperty('line.separator')

# source: http://setgetweb.com/p/WAS85x/ae/txml_listrunapp.html
cells = AdminConfig.list('Cell').split(lineSeparator)
for cell in cells:
  nodes = AdminConfig.list('Node', cell).split(lineSeparator)

  for node in nodes:
    cname = AdminConfig.showAttribute(cell, 'name')
    nname = AdminConfig.showAttribute(node, 'name')

    servs = AdminControl.queryNames('type=Server,cell=' + cname + ',node=' + nname + ',*').split(lineSeparator)
    print "Number of running servers on node " + nname + ": %s \n" % (len(servs))

    for server in servs:
      sname = AdminControl.getAttribute(server, 'name')
      ptype = AdminControl.getAttribute(server, 'processType')
      pid   = AdminControl.getAttribute(server, 'pid')
      state = AdminControl.getAttribute(server, 'state')
      jvm = AdminControl.queryNames('type=JVM,cell=' + cname + ',node=' + nname + ',process=' + sname + ',*')
      osname = AdminControl.invoke(jvm, 'getProperty', 'os.name')

      print " " + sname + " " +  ptype + " has pid " + pid + "; state: " + state + "; on " + osname + "\n"

      # source: https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-starting-listener-ports-using
      lPorts = AdminControl.queryNames('type=ListenerPort,cell=' + cname + ',node=' + nname + ',process=' + sname + ',*')

      if len(lPorts) == 0:
        print 'No listeners running on ' + node + ' ' + sname
      else:
        lPortsArray = lPorts.split(lineSeparator)
        for lPort in lPortsArray:
          state = AdminControl.getAttribute(lPort, 'started')
          lpcfgId = AdminControl.getConfigId(lPort)
          pName = AdminConfig.showAttribute(lpcfgId, 'name')
          if state != 'true':
            print pName + " Listener not running on " + sname
~
