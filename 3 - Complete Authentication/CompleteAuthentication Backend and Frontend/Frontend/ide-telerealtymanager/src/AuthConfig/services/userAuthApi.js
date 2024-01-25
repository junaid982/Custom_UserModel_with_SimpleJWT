import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { baseUrl } from '../baseUrls'
import { setUserToken, unSetUserToken } from '../features/authSlice'
import { getToken, removeToken, removeAllLocalStorageData } from './localStorageServices'


const baseQuery = fetchBaseQuery({
    baseUrl: baseUrl //set base url
})

const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions)
    const { refresh_token } = getToken()

    if (result?.error?.status === 401 | result?.error?.status === 403) {

        const urlHeader = {
            url: 'api/auth/token/refresh/',
            method: "POST",
            body: { 'refresh': refresh_token },
            headers: {
                'Content-type': "application/json"
            }
        }
        const refreshResult = await baseQuery(urlHeader, api, extraOptions)

        if (refreshResult.data) {

            localStorage.setItem('access_token', refreshResult.data.access)

            api.dispatch(setUserToken({ access_token: refreshResult.data.access, refresh_token: refresh_token }))

        } else {
            removeAllLocalStorageData()
            alert('Session time out !')
        }
    }
    return result
}


export const userAuthApi = createApi({

    reducerPath: 'userAuthApi',

    baseQuery: baseQueryWithReauth,

    endpoints: (builder) => ({

        // 1 - register user 
        registerUser: builder.mutation({
            query: ({ access_token, userRegisterData }) => {
                return {
                    url: 'api/auth/register-user/',
                    method: "POST",
                    body: userRegisterData,
                    headers: {
                        'Content-type': "application/json",
                        'authorization': `Bearer ${access_token}`
                    }
                }

            }
        }),

        // 2 - Login user 
        loginUser: builder.mutation({
            query: (loginData) => {
                return {
                    url: 'api/auth/user-login/',
                    method: "POST",
                    body: loginData,
                    headers: {
                        'Content-type': "application/json"
                    }
                }
            }
        }),


    }),
})

export const { useRegisterUserMutation, useLoginUserMutation } = userAuthApi
