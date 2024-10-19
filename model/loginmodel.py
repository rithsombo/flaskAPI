from flaskdemoo.config.dbconfig import PgConfig
#dto class
class LoginDto:
    __uname=None;
    __upass=None;
    __confirm_code=None;

    @property
    def ConfirmCode(self):
        return self.__confirm_code;

    @ConfirmCode.setter
    def ConfirmCode(self, value):
        self.__confirm_code = value;

    @property
    def Upass(self):
        return self.__upass;

    @Upass.setter
    def Upass(self, value):
        self.__upass = value;

    @property
    def Uname(self):
        return self.__uname;

    @Uname.setter
    def Uname(self, value):
        self.__uname = value;



#dao class
class LoginDao:
    def verifyAuth(self,dto):
        cur=PgConfig.getCursor(PgConfig);
        cur.execute("select * from usr.tbluser where is_active=true and uname=%s and upass=%s",(dto.Uname,dto.Upass))
        if(cur.rowcount>0):
            import random;
            val=random.randrange(100000, 999999)
            print("confirm code=",val)
            cur.execute("update usr.tbluser set confirm_code=%s,code_exp=now()+'2 minutes'::interval where is_active=true and uname=%s"
                        ,
                        (val,dto.Uname)
                        )
            PgConfig.Commit(PgConfig);
            return True
        else:
            return False;

    def confirmCode(self,dto):
        cur=PgConfig.getCursor(PgConfig);
        cur.execute(
            "select * from usr.tbluser where is_active=true and uname=%s and upass=%s and confirm_code=%s and now()<=code_exp",
            (dto.Uname, dto.Upass, dto.ConfirmCode))
        if(cur.rowcount>0):
            return True
        else:
            return False;

# dto=LoginDto();
# dto.Uname='admin'
# dto.Upass='123'
# dao=LoginDao();
# #result=dao.verifyAuth(dto)
# dto.ConfirmCode='9258671'
# result=dao.confirmCode(dto)
# print(result)