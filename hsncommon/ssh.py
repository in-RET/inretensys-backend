import paramiko
import sys
import asyncio
import asyncssh
import aiorun
import threading

from .log import HsnLogger
log = HsnLogger()

from .config import set_init_function_args_as_instance_args

class HsnSshConnectionConfig(object):
    def __init__(
        self,
        host : str = 'localhost',
        port : int = 22,
        keepalive : int = 60,
        username : str = None,
        password : str = None,
        user_directory : str = '/home',
        log : bool = False
    ):
        set_init_function_args_as_instance_args(self, locals())

    format = {
        'host' : 'str:256',
        'port' : 'int:1:65535:1',
        'keepalive' : 'int:1:3600:1',
        'username' : 'str:256',
        'password' : 'str:4096',
        'user_directory' : 'str:4096',
        'log' : 'bool'
    }


class HsnSshClientHandler(object):
    ## constructor
    def __init__(
        self,
        ssh_config : HsnSshConnectionConfig,
        *args,
        **kwargs
    ) -> None:
        self.__host = ssh_config.host
        self.__port = ssh_config.port
        self.__username = ssh_config.username
        self.__password = ssh_config.password
        self.__timeout = ssh_config.keepalive
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connected = False
        self.__log = ssh_config.log
        self.__connect()

    ## destructor
    def __del__(self):
        self.__ssh.close()


    # private interface methods
    ## connect to SSH remote server
    def __connect(self):
        assert(self.__host is not None and type(self.__host) == str)
        assert(self.__username is not None and type(self.__username) == str)
        assert(self.__password is not None and type(self.__password) == str)
        assert(self.__port is not None and type(self.__port) == int)
        assert(self.__timeout is not None and type(self.__timeout) == float)
        try:
            self.__ssh.connect(
                self.__host,
                port=self.__port,
                username=self.__username, 
                password=self.__password,
                timeout=self.__timeout
            )
            self.__connected = True
            if self.__log:
                log.info(f'ssh client connected to server {self.__host}:{self.__port}')
        except:
            self.__connected = False
    
    ## remotely execute command on ssh connection
    def __execute_cmd(self, cmd):
        if not self.__connected:
            return (None, None, False, 'ssh-client not connected')            

        stdout = None
        stderr = None
        success = False
        error = None

        try:
            _, stdout, stderr = self.__ssh.exec_command(cmd, get_pty=True)
            success = True
        except:
            success = False
            error = '{}'.format(sys.exc_info()[0])
        finally:
            return (stdout, stderr, success, error)

    # public interface methods
    def execute(self, cmd):
        stdout, stderr, success, error = self.__execute_cmd(cmd)

        if success == True:
            o = ''
            for line in stdout:
	            o += line            
            e = ''            
            for line in stderr:
                e += line
            return o, e, success, error
        else:
            return None, None, success, error

        return self.__execute_cmd(cmd)

    def connect(self):
        return self.__connect()

    def is_connected(self):
        return self.__connected




class HsnSftpClientHandler(object):
    ## constructor
    def __init__(
        self,
        sftp_config : HsnSshConnectionConfig,
        *args,
        **kwargs
    ) -> None:
        self.__host = sftp_config.host
        self.__port = sftp_config.port
        self.__username = sftp_config.username
        self.__password = sftp_config.password
        self.__timeout = sftp_config.keepalive
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connected = False
        self.__log = sftp_config.log
        self.__connect()


    ## destructor
    def __del__(self):
        self.__ssh.close()


    # private interface methods
    ## connect to SSH remote server
    def __connect(self):
        assert(self.__host is not None and type(self.__host) == str)
        assert(self.__username is not None and type(self.__username) == str)
        assert(self.__password is not None and type(self.__password) == str)
        assert(self.__port is not None and type(self.__port) == int)
        assert(self.__timeout is not None and type(self.__timeout) == int)
        try:
            self.__ssh.connect(
                self.__host,
                port=self.__port,
                username=self.__username, 
                password=self.__password,
                timeout=self.__timeout
            )
            self.__connected = True
            if self.__log:
                log.info(f'sftp client connected to server {self.__host}:{self.__port}')
        except:
            self.__connected = False

    ## send file over sftp
    def __send_file(self, local_path, remote_path):
        try:
            sftp = self.__ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            return True
        except:
            return False

    ## receive file over sftp
    def __receive_file(self, local_path, remote_path):
        try:
            sftp = self.__ssh.open_sftp()
            sftp.get(local_path, remote_path)
            sftp.close()
            return True
        except:
            return False

    # public interface methods
    def connect(self):
        return self.__connect()

    def is_connected(self):
        return self.__connected

    def send_file(self, remote_path, local_path):
        return self.__send_file(remote_path, local_path)

    def receive_file(self, remote_path, local_path):
        return self.__receive_file(remote_path, local_path)




class HsnAsyncSshClientHandler(object):
    def __init__(
        self,
        ssh_config : HsnSshConnectionConfig
    ) -> None:
        self.__conn_config = ssh_config

    def get_connection(self):
        return asyncssh.connect(self.__conn_config.host, username = self.__conn_config.username, password = self.__conn_config.password, known_hosts=None)
        
            
    async def run_async(self, stop, command, callback=None) -> None:
        log.trace('async ssh command start')
        async with self.get_connection() as c:
            log.trace('async ssh connection established')
            log.trace(f'async ssh thread:{threading.current_thread().name}')
            try:
                async with c.create_process(command, term_type='dumb') as p:
                    log.trace('async ssh process started')
                    async for line in p.stdout:
                        if line and line != '':
                            if callback:
                                await callback(line.strip('\n'))
            except (OSError, asyncssh.Error) as exc:
                log.trace(f'{self.__conn_config.host}: CONNECTION FAILED: {exc}')
                    
    async def run_sync(self, command) -> None:
        stdout = ''
        async with self.get_connection() as c:
            async with c.create_process(command, term_type='dumb') as p:
                async for line in p.stdout:
                    stdout += line
        return stdout


    '''    
    async def put_file(self, local_file, remote_file, callback=None) -> None:
        async with asyncssh.connect(self.__conn_config.host, username = self.__conn_config.username, password = self.__conn_config.password, known_hosts=None) as c:
            async with c.start_sftp_client() as sftp:
                await sftp.put(local_file, remote_file)
                if callback:
                    callback()
                

    async def get_file(self, remote_file, local_path, callback=None) -> None:
        async with asyncssh.connect(self.__conn_config.host, username = self.__conn_config.username, password = self.__conn_config.password, known_hosts=None) as c:
            async with c.start_sftp_client() as sftp:
                await sftp.get(remote_file, local_path)
                if callback:
                    callback()
    '''

    def run_async_command(self, stop, command, callback=None):
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(self.run_async(stop, command, callback))

        #aiorun.run(self.__run_async_command(stop, command, callback))

    def run_sync_command(self, stop, command, callback=None):
        loop = asyncio.new_event_loop()
        loop.set_debug(True)
        retval = loop.run_until_complete(self.run_sync(command))
        if callback:
            callback(retval)