#!/usr/bin/python3
import bcrypt


class Hash:
    def hash_password(password):
        '''Hash a password with the default bcrypt algorithm. Autmatically encodes and transforms data into bytes

        Args:
        password -> Hashable data type
        ''' 
         
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password


    def verify_password(plain_password, hashed_password):
        '''Args:
        
        plain_password -> unencryped password (plain data)
        hashed_password -> encrypted password'''
        
        password_byte_enc = plain_password.encode('utf-8')
        return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)