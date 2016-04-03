/*
	Radiobeacon - Openbmap wifi and cell logger
    Copyright (C) 2013  wish7

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package org.openbmap.commands;

import android.app.Activity;
import android.widget.Toast;

import org.greenrobot.eventbus.EventBus;
import org.openbmap.R;
import org.openbmap.events.onStopTracking;

/**
 * Dispatcher for external 'stop tracking' command
 * E.g. sent by external NFC apps like https://play.google.com/store/apps/details?id=com.jwsoft.nfcactionlauncher
 *
 * Don't use internally within Radiobeacon!
 */
public class StopTracking  extends Activity {

	@Override
	protected final void onResume() {
		super.onResume();

        EventBus.getDefault().post(new onStopTracking());
		Toast.makeText(this, R.string.stopped_tracking, Toast.LENGTH_SHORT).show();
		this.finish();
	}



}
