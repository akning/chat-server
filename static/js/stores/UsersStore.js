import { EventEmitter } from 'events';

import dispatcher from '../dispatcher';

class UsersStore extends EventEmitter {
    constructor() {
        super();
        this.usersList = [
            {
                name: 'Select a user...',
                timeStamp: null
            }
        ];
    }

    getUsername(name) {
        for(var i = 1; i < this.usersList.length; i++) {
            if (name === this.usersList[i].name) {
                this.usersList[i].timeStamp = Date.now();
                this.emit('updateUsersList');
                return;
            }
        }
        console.log('name does not equal.');
        this.usersList.push({
            name,
            timeStamp: Date.now()
        });

        this.emit('updateUsersList');
    }

    popUsername() {
        setInterval(
            () => {
                for(var i = 1; i < this.usersList.length; i++) {
                    if (Date.now() - this.usersList[i].timeStamp > 3500) {
                        this.usersList.splice(i, 1);
                        console.log('This user is offline. So, byebye.');
                        this.emit('updateUsersList');
                    }
                }
            },
        3000);
    }

    getAll() {
        return this.usersList;
    }

    handleActions(action) {
        switch(action.type) {
            case 'PUSH_USERNAME': {
                this.getUsername(action.name);
            }
            case 'POP_USERNAME': {
                this.popUsername();
            }
        }
    }
}

const usersStore = new UsersStore;
dispatcher.register(usersStore.handleActions.bind(usersStore));
export default usersStore;
