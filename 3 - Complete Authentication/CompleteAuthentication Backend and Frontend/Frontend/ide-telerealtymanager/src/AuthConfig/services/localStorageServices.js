// to store tokens into a local storage 
const storeToken = (value) => {

    if (value) {

        const { access, refresh } = value
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
    }
}


// to access tokens from localstorage 
const getToken = () => {
    let access_token = localStorage.getItem('access_token')
    let refresh_token = localStorage.getItem('refresh_token')

    return { access_token, refresh_token }
}


// to remove token from local storage 
const removeToken = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')

}


const storeUserProfile = (userData) => {
    if (userData) {
        const { id, name, email, designation, user_roll, user_profile, is_active, is_staff, is_admin, dashboard_perms, sheets_perms, uploads_perms, users_perms,
            activity_perms, other_perms, created_at, updated_at } = userData

        localStorage.setItem('userId', id)
        localStorage.setItem('userName', name)
        localStorage.setItem('userEmail', email)
        localStorage.setItem('userDesignation', designation)
        localStorage.setItem('userRoll', user_roll)
        localStorage.setItem('userProfile', user_profile)
        localStorage.setItem('userIsActive', is_active)
        localStorage.setItem('userIsStaff', is_staff)
        localStorage.setItem('userIsAdmin', is_admin)
        localStorage.setItem('userDashboardPerms', dashboard_perms)
        localStorage.setItem('userSheetPerms', sheets_perms)
        localStorage.setItem('userUplooadPerms', uploads_perms)
        localStorage.setItem('userUsersPerms', users_perms)
        localStorage.setItem('userActivityPerms', activity_perms)
        localStorage.setItem('userOtherPerms', other_perms)
        localStorage.setItem('userCreatedAt', created_at)
        localStorage.setItem('userUpdatedAt', updated_at)

    }

}

const getUserProfile = () => {

    let userId = localStorage.getItem('userId')
    let userName = localStorage.getItem('userName')
    let userEmail = localStorage.getItem('userEmail')
    let userDesignation = localStorage.getItem('userDesignation')
    let userRoll = localStorage.getItem('userRoll')
    let userProfile = localStorage.getItem('userProfile')
    let userIsActive = localStorage.getItem('userIsActive')
    let userIsStaff = localStorage.getItem('userIsStaff')
    let userIsAdmin = localStorage.getItem('userIsAdmin')
    let userDashboardPerms = localStorage.getItem('userDashboardPerms')
    let userSheetPerms = localStorage.getItem('userSheetPerms')
    let userUplooadPerms = localStorage.getItem('userUplooadPerms')
    let userUsersPerms = localStorage.getItem('userUsersPerms')
    let userActivityPerms = localStorage.getItem('userActivityPerms')
    let userOtherPerms = localStorage.getItem('userOtherPerms')
    let userCreatedAt = localStorage.getItem('userCreatedAt')
    let userUpdatedAt = localStorage.getItem('userUpdatedAt')

    return {
        userId, userName, userEmail, userDesignation, userRoll, userProfile, userIsActive,
        userIsStaff, userIsAdmin, userDashboardPerms, userSheetPerms, userUplooadPerms, userUsersPerms,
        userActivityPerms, userOtherPerms, userCreatedAt, userUpdatedAt
    }
}


const removeAllLocalStorageData = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('userId')
    localStorage.removeItem('userName')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userDesignation')
    localStorage.removeItem('userRoll')
    localStorage.removeItem('userProfile')
    localStorage.removeItem('userIsActive')
    localStorage.removeItem('userIsStaff')
    localStorage.removeItem('userIsAdmin')
    localStorage.removeItem('userDashboardPerms')
    localStorage.removeItem('userSheetPerms')
    localStorage.removeItem('userUplooadPerms')
    localStorage.removeItem('userUsersPerms')
    localStorage.removeItem('userActivityPerms')
    localStorage.removeItem('userOtherPerms')
    localStorage.removeItem('userCreatedAt')
    localStorage.removeItem('userUpdatedAt')
}

const storeNewAccessToken = (accessJson) => {

    const { access } = accessJson

    localStorage.setItem('access_token', access)

}

export { storeToken, getToken, removeToken, storeUserProfile, getUserProfile, removeAllLocalStorageData, storeNewAccessToken }