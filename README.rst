thoth-s2i-demo
--------------

An example repository of a project to show how to migrate an already existing
OpenShift Python s2i application to Thoth (demo).

See `https://thoth-station.ninja <https://thoth-station.ninja>`_ for more info
on Thoth.

Usage
=====

The application is created out of this repository. It follows OpenShift Python
s2i build process. The built application is a simple TensorFlow application
that prints ``"Hello, Thoth!"`` to the console using TensorFlow.

Mind the ``app.py`` and ``requirements.txt`` files needed for the application
present in the Git repository.  The ``openshift.yaml`` file is a manifest used
to deploy this application to an OpenShift cluster.

Installation
============

Log in to an OpenShift cluster and select namespace you would like to use:

.. code-block:: console

  oc login
  oc project thoth-s2i-demo

To install this application to an OpenShift cluster run the following command:

.. code-block:: console

  oc create -f https://raw.githubusercontent.com/fridex/thoth-s2i-demo/master/openshift.yaml

Migrating to Thoth
==================

To migrate this application to Thoth, use a tool called `thoth-s2i
<https://pypi.org/project/thoth-s2i>`_:

.. code-block:: console

  pip install thoth-s2i

.. note::

  The `oc` binary needs to be installed on your system and you need to be logged
  in into an OpenShift cluster in order to follow the upcomming steps.

First, let's have a look at the namespace - what build configs are present and
ready to be migrated:

.. code-block:: console

  thoth-s2i report --namespace thoth-s2i-demo
  2020-04-29 16:04:48,903 [218204] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmp5x6eiurw'
  2020-04-29 16:04:48,917 [218204] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'buildconfig' in '/tmp/tmp5x6eiurw'
  2020-04-29 16:04:50,041 [218204] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmp5x6eiurw'
  2020-04-29 16:04:50,069 [218204] INFO     thoth.s2i.objs: Found 'python-36' of kind 'imagestream' in '/tmp/tmp5x6eiurw'
  2020-04-29 16:04:50,069 [218204] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'imagestream' in '/tmp/tmp5x6eiurw'
  2020-04-29 16:04:50,070 [218204] INFO     thoth.s2i.objs: Found 's2i-thoth-ubi8-py36' of kind 'imagestream' in '/tmp/tmp5x6eiurw'
  📝 s2i-example-tensorflow
  	🠒 strategy: 'Source'
  	🠒 image_stream: 'python-36'
  	🠒 image_stream_tag: 'latest'
  	🠒 is_s2i: True
  	🠒 s2i_image_name: 'registry.access.redhat.com/ubi8/python-36'
  	🠒 s2i_image_tag: 'latest'

The report printed aggregates information about the namespace in a human
readable form (see options available to adjust output based on label selector
or to create JSON/YAML output).

Now, let's check what Thoth s2i container images are available:

.. code-block:: console

  thoth-s2i images
  ✔ quay.io/thoth-station/s2i-thoth-ubi8-py36
  ✔ quay.io/thoth-station/s2i-thoth-f31-py37

Next, let's issue a dry run migration so we know what changes the tool will make
to the cluster. We choose ``s2i-thoth-ubi-py36`` as a Python s2i drop-in
replacement of the UBI 8 Python 3.6 container image we are already using in the
deployment:

.. code-block:: console

  thoth-s2i migrate -n thoth-s2i-demo --dry-run --insert-env-vars --s2i-thoth quay.io/thoth-station/s2i-thoth-ubi8-py36
  2020-04-29 16:21:44,455 [220851] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmp5hmcksot'
  2020-04-29 16:21:44,481 [220851] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'buildconfig' in '/tmp/tmp5hmcksot'
  2020-04-29 16:21:44,481 [220851] INFO     thoth.s2i.lib: Patching BuildConfig 's2i-example-tensorflow', replacing 'python-36:latest' with 's2i-thoth-ubi8-py36:latest'
  2020-04-29 16:21:44,481 [220851] INFO     thoth.s2i.objs: Inserting Thoth and Thamos specific environment variables to 's2i-example-tensorflow'
  2020-04-29 16:21:44,482 [220851] WARNING  thoth.s2i: Dry run will not import image into OpenShift's registry
  --
  apiVersion: build.openshift.io/v1
  kind: BuildConfig
  metadata:
    creationTimestamp: '2020-04-29T14:03:57Z'
    labels:
      app: s2i-example-tensorflow
    name: s2i-example-tensorflow
    namespace: thoth-s2i-demo
    resourceVersion: '4545199'
    selfLink: /apis/build.openshift.io/v1/namespaces/thoth-s2i-demo/buildconfigs/s2i-example-tensorflow
    uid: 72224227-fd18-49e9-aa91-2661cb1da325
  spec:
    failedBuildsHistoryLimit: 2
    nodeSelector: null
    output:
      to:
        kind: ImageStreamTag
        name: s2i-example-tensorflow:latest
    postCommit: {}
    resources:
      limits:
        cpu: '1'
        memory: 1Gi
      requests:
        cpu: '1'
        memory: 1Gi
    runPolicy: Serial
    source:
      git:
        ref: master
        uri: https://github.com/fridex/thoth-s2i-demo
      type: Git
    strategy:
      sourceStrategy:
        env:
        - name: ENABLE_PIPENV
          value: '1'
        - name: UPGRADE_PIP_TO_LATEST
          value: ''
        - name: THOTH_DRY_RUN
          value: '0'
        - name: THOTH_ADVISE
          value: '1'
        - name: THOTH_ASSEMBLE_DEBUG
          value: '1'
        - name: THOTH_FROM_MASTER
          value: '0'
        - name: THOTH_ERROR_FALLBACK
          value: '1'
        - name: THAMOS_VERBOSE
          value: '0'
        - name: THAMOS_FORCE
          value: '0'
        - name: THAMOS_DEBUG
          value: '0'
        - name: THAMOS_CONFIG_EXPAND_ENV
          value: '0'
        - name: THAMOS_NO_PROGRESSBAR
          value: '1'
        - name: THAMOS_NO_INTERACTIVE
          value: '1'
        - name: THAMOS_DEV
          value: '0'
        from:
          kind: ImageStreamTag
          name: s2i-thoth-ubi8-py36:latest
      type: Source
    successfulBuildsHistoryLimit: 1
    triggers:
    - imageChange:
        lastTriggeredImageID: registry.access.redhat.com/ubi8/python-36@sha256:7c29ae7f78f2f899b743455fdc6e8068c0ac18a27fdae58ce3123acdc116b087
      type: ImageChange
  status:
    lastVersion: 1

Based on the output, we see changes in the builder image - now we use
``ImageStreamTag`` named ``s2i-thoth-ubi8-py36:latest``. We also see Thoth
specific configuration options present in the environment variables of the
build config. To understand their semantics, refer to `s2i-thoth
<https://github.com/thoth-station/s2i-thoth>`_ documentation and `Thamos
<https://github.com/thoth-station/thamos>`_.

After the changes done have been reviewed, we can submit them to the cluster by
removing the ``--dry-run`` option:

.. code-block:: console

  thoth-s2i migrate -n thoth-s2i-demo --insert-env-vars --s2i-thoth quay.io/thoth-station/s2i-thoth-ubi8-py36 --import-image --trigger-build
  2020-04-29 16:26:27,857 [221257] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmpu46k0k9n'
  2020-04-29 16:26:27,885 [221257] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'buildconfig' in '/tmp/tmpu46k0k9n'
  2020-04-29 16:26:27,885 [221257] INFO     thoth.s2i.lib: Patching BuildConfig 's2i-example-tensorflow', replacing 'python-36:latest' with 's2i-thoth-ubi8-py36:latest'
  2020-04-29 16:26:27,885 [221257] INFO     thoth.s2i.objs: Inserting Thoth and Thamos specific environment variables to 's2i-example-tensorflow'
  2020-04-29 16:26:27,886 [221257] INFO     thoth.s2i.objs: Applying changes made to 's2i-example-tensorflow' to the cluster
  2020-04-29 16:26:32,727 [221257] INFO     thoth.s2i.objs: Triggering build for 's2i-example-tensorflow' in namespace 'thoth-s2i-demo'
  imagestream.image.openshift.io/s2i-thoth-ubi8-py36 imported
  
  Name:			s2i-thoth-ubi8-py36
  Namespace:		thoth-s2i-demo
  Created:		2 hours ago
  Labels:			app=s2i-example-tensorflow
  Annotations:		kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"image.openshift.io/v1","kind":"ImageStream","metadata":{"annotations":{},"labels":{"app":"s2i-example-tensorflow"},"name":"s2i-thoth-ubi8-py36","namespace":"thoth-s2i-demo"},"spec":{"tags":[{"from":{"kind":"DockerImage","name":"quay.io/thoth-station/s2i-thoth-ubi8-py36"},"name":"latest","referencePolicy":{"type":"Source"}}]}}
  
  			openshift.io/image.dockerRepositoryCheck=2020-04-29T12:52:23Z
  Docker Pull Spec:	image-registry.openshift-image-registry.svc:5000/thoth-s2i-demo/s2i-thoth-ubi8-py36
  Image Lookup:		local=false
  Unique Images:		1
  Tags:			1
  
  latest
    tagged from quay.io/thoth-station/s2i-thoth-ubi8-py36
  
    * quay.io/thoth-station/s2i-thoth-ubi8-py36@sha256:1d7d42821cfdb30d9ca5f8da488741c02f87a75ffe9ef32d2bccb2f5a0005321
        2 hours ago
  
  Image Name:	s2i-thoth-ubi8-py36:latest
  Docker Image:	quay.io/thoth-station/s2i-thoth-ubi8-py36@sha256:1d7d42821cfdb30d9ca5f8da488741c02f87a75ffe9ef32d2bccb2f5a0005321
  Name:		sha256:1d7d42821cfdb30d9ca5f8da488741c02f87a75ffe9ef32d2bccb2f5a0005321
  Created:	22 seconds ago
  Annotations:	image.openshift.io/dockerLayersOrder=ascending
  Image Size:	289.8MB in 7 layers
  Layers:		74.02MB	sha256:78afc5364ad2c981e4a4919f535aaefef9ac2f990837be01c766764e025b1f31
  		1.564kB	sha256:58e1deb9693dfb1704ccce2f1cf0e4d663ac77098a7a0f699708a71549cbd924
  		16.67MB	sha256:1d3caaab0e6b8f6421152e3e992b9af724fb775da1fbc232ce24b02d5a910efd
  		124.6MB	sha256:a4de40bef32d2d442436fd227ae0ff8950dff0bb8f2861e8d6550ed5d54d0b11
  		55.32MB	sha256:7e39dc43e16c66fcceffdded184903e157be1091e8829983007b3c946c094c76
  		702B	sha256:333a0e4d4b1fa5f0d37144430383144f26b1f9f86884b254658f353c829400be
  		19.22MB	sha256:dd89c8518b4768ce3f9fd29940f0e0548609a371d416ddf5622864d9bd5ea872
  Image Created:	6 hours ago
  Author:		<none>
  Arch:		amd64
  Entrypoint:	container-entrypoint
  Command:	/bin/sh -c $STI_SCRIPTS_PATH/usage
  Working Dir:	/opt/app-root/src
  User:		1001
  Exposes Ports:	8080/tcp
  Docker Labels:	architecture=x86_64
  		build-date=2020-04-23T10:39:48.254767
  		com.redhat.build-host=cpt-1001.osbs.prod.upshift.rdu2.redhat.com
  		com.redhat.component=python-36-container
  		com.redhat.license_terms=https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI
  		description=Thoth's Source-to-Image for Python 3.6 applications. This toolchain is based on Red Hat UBI8. It includes pipenv.
  		distribution-scope=public
  		io.k8s.description=Thoth's Source-to-Image for Python 3.6 applications. This toolchain is based on Red Hat UBI8. It includes pipenv.
  		io.k8s.display-name=Thoth Python 3.6-ubi8 S2I
  		io.openshift.expose-services=8080:http
  		io.openshift.s2i.scripts-url=image:///usr/libexec/s2i
  		io.openshift.tags=python,python36
  		io.s2i.scripts-url=image:///usr/libexec/s2i
  		maintainer=Thoth Station <aicoe-thoth@redhat.com>
  		name=thoth-station/s2i-thoth-ubi8-py36:v0.12.0
  		ninja.thoth-station.version=0.6.0-dev
  		release=0
  		summary=Thoth's Source-to-Image for Python 3.6 applications
  		url=https://access.redhat.com/containers/#/registry.access.redhat.com/ubi8/python-36/images/1-89
  		usage=s2i build https://github.com/sclorg/s2i-python-container.git --context-dir=3.6/test/setup-test-app/ ubi8/python-36 python-sample-app
  		vcs-ref=cc087e1dcb33f4838e0a939b20a384149a70bc99
  		vcs-type=git
  		vendor=AICoE at the Office of the CTO, Red Hat Inc.
  		version=0.12.0
  Environment:	PATH=/opt/app-root/src/.local/bin/:/opt/app-root/src/bin:/opt/app-root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
  		container=oci
  		SUMMARY=Thoth's Source-to-Image for Python 3.6 applications
  		DESCRIPTION=Thoth's Source-to-Image for Python 3.6 applications. This toolchain is based on Red Hat UBI8. It includes pipenv.
  		STI_SCRIPTS_URL=image:///usr/libexec/s2i
  		STI_SCRIPTS_PATH=/usr/libexec/s2i
  		APP_ROOT=/opt/app-root
  		HOME=/opt/app-root/src
  		PLATFORM=el8
  		NODEJS_VER=10
  		PYTHON_VERSION=3.6
  		PYTHONUNBUFFERED=1
  		PYTHONIOENCODING=UTF-8
  		LC_ALL=en_US.UTF-8
  		LANG=en_US.UTF-8
  		PIP_NO_CACHE_DIR=off
  		BASH_ENV=/opt/app-root/etc/scl_enable
  		ENV=/opt/app-root/etc/scl_enable
  		PROMPT_COMMAND=. /opt/app-root/etc/scl_enable
  		THOTH_S2I_VERSION=v0.12.0
  		THAMOS_NO_PROGRESSBAR=1
  		THAMOS_NO_EMOJI=1

We also added ``--import-image`` option so that ``s2i-thoth-ubi-8-py36`` is
imported to the namespace and available via OpenShift's image stream. The
``--trigger-build`` option makes sure all the builds are triggered on this
change even if the ``BuildConfig`` has no configuration change build trigger
set up.

To double check changes, we can ask for the cluster report again:

.. code-block:: console

  thoth-s2i report -n thoth-s2i-demo   
  2020-04-29 16:27:43,860 [221475] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmpvx34u93m'
  2020-04-29 16:27:43,885 [221475] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'buildconfig' in '/tmp/tmpvx34u93m'
  2020-04-29 16:27:44,936 [221475] INFO     thoth.s2i.objs: Loading file content from '/tmp/tmpvx34u93m'
  2020-04-29 16:27:44,979 [221475] INFO     thoth.s2i.objs: Found 'python-36' of kind 'imagestream' in '/tmp/tmpvx34u93m'
  2020-04-29 16:27:44,979 [221475] INFO     thoth.s2i.objs: Found 's2i-example-tensorflow' of kind 'imagestream' in '/tmp/tmpvx34u93m'
  2020-04-29 16:27:44,980 [221475] INFO     thoth.s2i.objs: Found 's2i-thoth-ubi8-py36' of kind 'imagestream' in '/tmp/tmpvx34u93m'
  📝 s2i-example-tensorflow
  		🠒 strategy: 'Source'
  		🠒 image_stream: 's2i-thoth-ubi8-py36'
  		🠒 image_stream_tag: 'latest'
  		🠒 is_s2i: True
  		🠒 is_s2i_thoth: True
  		🠒 s2i_image_name: 'quay.io/thoth-station/s2i-thoth-ubi8-py36'
  		🠒 s2i_image_tag: 'latest'
  
Clean up
========

To remove this application from the namespace:

.. code-block:: console

  oc delete -f https://raw.githubusercontent.com/fridex/thoth-s2i-demo/master/openshift.yaml
  # Or, alternatively:
  #   oc delete bc,dc,is -l app=s2i-example-tensorflow
