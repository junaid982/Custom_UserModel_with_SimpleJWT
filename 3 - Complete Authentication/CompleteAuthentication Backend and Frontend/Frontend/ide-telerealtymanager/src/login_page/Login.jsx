
import React, { useState } from 'react';
import { Form, Input, Typography, Button, Alert } from 'antd';
import { UserOutlined, LockOutlined, EyeTwoTone, EyeInvisibleOutlined, } from '@ant-design/icons'

import './Login.css';

// Import APi Hook for Login 
import { useLoginUserMutation } from '../AuthConfig/services/userAuthApi';
import { useDispatch } from 'react-redux';
import { getToken, storeToken, storeUserProfile } from '../AuthConfig/services/localStorageServices';
import { setUserToken } from '../AuthConfig/features/authSlice';

const Login = () => {


    const [userEmail, setUserEmail] = useState('') //store user email
    const [userPassword, setUserPassword] = useState('') //store user password
    // State to show Alert Mesg for login success and login failure
    const [loginError, setLoginError] = useState(
        {
            state: false,
            msg: "",
            error: ""
        }
    );



    // Destructure APi Mutation for api call
    const [loginUser, { isLoading }] = useLoginUserMutation();
    const dispatch = useDispatch();

    const handleLoginForm = async (e) => {
        e.preventDefault();

        // prepare data for api call
        if (!userEmail && !userPassword) {
            return false
        }
        else {

            const loginData = {
                email: userEmail,
                password: userPassword
            }

            const res = await loginUser(loginData);
            // console.log("res :", res)

            if (res?.data) {

                // show success message
                setLoginError(
                    {
                        state: true,
                        msg: "Login Successful",
                        error: "success"
                    }
                )

                setTimeout(() => {
                    handleClearErrorMsg()
                }, 5000)

                // store token in local storage
                storeToken(res.data.token)

                // store user details in local storage
                storeUserProfile(res.data.user_data)

                // Store token into a redux state
                let { access_token, refresh_token } = getToken()
                dispatch(setUserToken({ access_token: access_token, refresh_token: refresh_token }))

                // Navigation to dashboard page


            }
            else if (res?.error) {
                console.log("Error :", res.error.data.error)

                // show success message
                setLoginError(
                    {
                        state: true,
                        msg: res.error.data.error,
                        error: "error"
                    }
                )

            }

        }



    }

    // clear Error msg 
    const handleClearErrorMsg = () => {
        setLoginError({
            state: false,
            msg: "",
            error: ""
        })
    }

    return (
        <div className='login-page-container'>

            <div className='login-form-container'>

                <Form className='loginForm' id='loginForm' onSubmitCapture={handleLoginForm} >
                    <div className='errorBox'>
                        <Typography.Title style={{ textAlign: "center" }} className='form-heading'>IDE TeleRealty Manager</Typography.Title>
                    </div>

                    {/* Alert Msg For Login and Error  */}
                    {loginError.state ?
                        <Alert message={loginError.msg} style={{ marginBottom: 20 }} type={loginError.error} closable onClose={handleClearErrorMsg} />
                        : ''
                    }


                    {/* Login Form  */}

                    <div className='form-content'>
                        <Form.Item
                            rules={[{ required: true, type: "email", message: "Please enter valid email" }]}
                            name={"email"}>

                            <Input className='mail' placeholder="Email" prefix={<UserOutlined />}
                                // onChange={(e) => { setUserEmail(e.target.value) }}
                                onChange={(e) => { setUserEmail(e.target.value) }}
                            />
                        </Form.Item>

                    </div>

                    <div className='form-content'>

                        <Form.Item
                            rules={[{ required: true, max: 15, min: 5, message: "Please enter valid password" }]}
                            name={"password"}>

                            <Input.Password className='mail' placeholder="password" prefix={<LockOutlined />}
                                iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                                onChange={(e) => { setUserPassword(e.target.value) }}
                            />

                        </Form.Item>

                    </div>

                    <div className='form-btn-content'>

                        <Button type="primary" htmlType="submit" className='login-btn'>Login</Button>

                    </div>

                </Form>




            </div>


            {/* Login footer  */}
            <div className="login-footer">
                <Typography className='login-footer-text'>
                    Powered By ItsDigitalEra.in
                </Typography>
            </div>



        </div>
    );
}

export default Login;