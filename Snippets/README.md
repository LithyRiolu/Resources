###### The Lithe Project&trade; Development Team

## Snippets

### Contents

- [CryptoNote Testnet Fix](https://github.com/LithyRiolu/lithe/commit/e962cb07dc89b2c3ad0d50587aa61f780d4f6e01) 
- [flow.flowconfig](https://github.com/LithyRiolu/Resources/blob/master/Snippets/flow.flowconfig) - [about](https://github.com/LithyRiolu/Resources/tree/master/Snippets#flowconfig)
- [PyMiner.py](https://github.com/LithyRiolu/Resources/blob/master/Snippets/PyMiner.py) - [about](https://github.com/LithyRiolu/Resources/tree/master/Snippets#pyminer)

### Usage

#### CryptoNote Testnet Fix
I believe, after working on a few cryptonote projects, that if the arg `--testnet` is still used within the core daemon,
then the upgrade height isn't going past `major_version: 2` when you call `/getInfo`. In order for the `--testnet` flag to
remain relevent and useful within the daemon, then more parameters have to be placed. Currently, they're setup like so;

```cpp
if (isTestnet()) {
    m_upgradeHeightV2 = 0;
    m_upgradeHeightV3 = static_cast<uint32_t>(-1);
}
```
This makes `m_upgradeHeightV3` not *hardfork* in the testnet. In my notes on Lithe, I've explained why `m_upgradeHeightV2 = 0;`
is okay in this situation but `m_upgradeHeightV3` would need to be updated to an actual index. So, if we change (and add) this
to this;

```cpp
if (isTestnet()) {
    m_upgradeHeightV2 = 0;
    m_upgradeHeightV3 = 1;
    m_upgradeHeightV4 = 2; /* @NOTE: This is where you would add hardforks to the testnet */
    /* and so on... */
}
```
Now, if we're running a daemon using the `--testnet` flag, when calling `/getInfo` you should see it has actually *hardforked*.
**@NOTE:** This is a relevent discovery because some projects out there have had problems with hardforks because something went
wrong on the chain, this should hopefully resolve and help many other CryptoNote projects.


#### Flowconfig
Used to bypass `ELIFECYCLE` error when running `npm install`

- Place `flow.flowconfig` within root of NodeJS project (where you would `npm install`).
- Run `sudo npm install -g flow-typed`

#### PyMiner
A simple python miner script optimized for TurtleCoin and its forks. 
