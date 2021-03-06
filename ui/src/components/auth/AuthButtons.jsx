import React, {Component} from 'react';
import {Button} from '@blueprintjs/core';
import {FormattedMessage} from 'react-intl';
import {Link} from 'react-router-dom';


class AuthButtons extends Component {
  render() {
    const { session, auth } = this.props;
    const location = window.location;
    const targetUrl = `${location.protocol}//${location.host}/login`;
    const loginUrlQueryString = `?next=${encodeURIComponent(targetUrl)}`;
    const items = [];

    if (session.loggedIn) {
      return <Link to="/logout">
        <Button iconName="log-out" className="pt-minimal">
          <FormattedMessage id="nav.signout" defaultMessage="Log out"/>
        </Button>
      </Link>
    }

    if (auth.oauth_uri) {
      items.push((
        <a key='oauth' href={`${auth.oauth_uri}${loginUrlQueryString}`}>
          <Button iconName="user" className="pt-minimal">
            <FormattedMessage id="login.oauth" defaultMessage="Sign in" />
          </Button>
        </a>
      ))
    }

    if (auth.password_login_uri) {
      items.push((
        <Link key='login' to="/login">
          <Button iconName="user" className="pt-minimal">
            <FormattedMessage id="nav.signin" defaultMessage="Log in"/>
          </Button>
        </Link>
      ))
    }

    if (auth.registration_uri) {
      items.push((
        <Link key='signup' to="/signup">
          <Button iconName="user" className="pt-minimal">
            <FormattedMessage id="nav.signup" defaultMessage="Register"/>
          </Button>
        </Link>
      ))
    }

    return (
      <span>{items}</span>
    )
  }
}

export default AuthButtons;
