import yaml
import os

def parse_entities_configs(path: str, logger=None) -> dict:

    if not os.path.exists(path):
        msg='Path {} does not exist.'.format(path)
        if logger is not None:
            logger.error(msg)
        else:
            print(msg)
            return FileExistsError(msg)

    if os.path.isfile(path):
        files = [path]
    else:
        files = os.listdir(path)

    if len(files) == 0:
        msg = 'No files found in directory {}.'.format(path)
        if logger is not None:
            logger.error(msg)
        else:
            raise FileNotFoundError(msg)

    out = dict()

    for file in files:
        fp = os.path.join(path, file)
        msg='Parsing entities configuration file {}'.format(fp)
        if logger is not None:
            logger.info(msg)
        else:
            print(msg)
        with open(fp, 'r') as stream:
            try:
                data=yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                msg='Cannot load entities configuration file safely. Reason: {}'.format(str(exc))
                if logger is not None:
                    logger.error(msg)
                else:
                    print(msg)
                continue

        track=['track' in d.keys() for d in data]

        if not all(track):
            idx=[i for i in range(len(track)) if not track[i]]
            sidx=[str(i+1) for i in idx]
            msg='Some entries are missing a "track" key (entries: {}). '.format(', '.join(sidx))
            msg+='Assuming that these entities should be tracked.'
            if logger is not None:
                logger.warning(msg)
            else:
                print(msg)
            for i in idx:
                data[i]['track']=True

        out[fp]=list()
        for d in data:
            if d['track']:
                for key, val in d.items():
                    out[fp].append({'username': val, 'kind': key})
                    # break after first
                    break

    return out
